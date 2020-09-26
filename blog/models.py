from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models, IntegrityError, ProgrammingError, OperationalError
from django.db.models import Q, Sum
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from django_q.tasks import Schedule
from markdownx.models import MarkdownxField
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel

from core.utils import get_current_domain_url
from newsletter.models import News
from .utils import queryset_index_of

User = get_user_model()


class Postable(models.Model):
    thumbnail = models.OneToOneField(
        "core.Thumbnail", blank=True, null=True, on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=150)
    overview = MarkdownxField()
    body = MarkdownxField(blank=True)
    slug = AutoSlugField(populate_from=["title"])
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Category(TimeStampedModel):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_list_url(self):
        url = reverse("blog:post_list") + f"?category={self.name}"
        return url

    @property
    def posts_count(self):
        return Post.objects.filter(
            categories__name=self.name, status=Post.STATUS.published
        ).count()


class Post(Postable, StatusModel, TimeStampedModel, SoftDeletableModel):
    STATUS = Choices("draft", "published")
    status = StatusField(default=STATUS.draft)
    status_changed = MonitorField(monitor="status")
    categories = models.ManyToManyField(Category)
    reading_time = models.IntegerField()
    publish_date = models.DateTimeField(null=True, blank=True)
    scheduled_publish_date = models.DateTimeField(null=True, blank=True)
    series = models.ForeignKey(
        "blog.Series", null=True, blank=True, on_delete=models.SET_NULL
    )

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def is_published(self):
        return self.status == Post.STATUS.published

    @property
    def next_post(self):
        if not self.series:
            return None
        posts = self.series.all_blogpost().filter(status=Post.STATUS.published)
        if self == posts.last() or self not in posts:
            return None
        return posts[queryset_index_of(posts, self) + 1]

    @property
    def previous_post(self):
        if not self.series:
            return None
        posts = self.series.all_blogpost().filter(status=Post.STATUS.published)
        if self == posts.first() or self not in posts:
            return None
        return posts[queryset_index_of(posts, self) - 1]

    def belongs_to_series(self, series):
        return self.series == series

    def publish(self, *args, **kwargs):
        self.status = Post.STATUS.published
        self.publish_date = timezone.now()
        self.save()
        self.send_publish_email(request=kwargs.get("request", None))

    def send_publish_email(self, **kwargs):
        # TODO write a decent email for publish post
        # send email to subscribers to inform of new post
        subject = "New Blog Post"
        message = render_to_string(
            "blog/email/new_post_message.html",
            context={
                "title": self.title,
                "link": f"{get_current_domain_url()}{self.get_absolute_url()}",
                "email": self.author.email,
                "twitter": self.author.profile.twitter,
                "github": self.author.profile.github,
                "telegram": self.author.profile.telegram,
            },
        ).format("utf-8")
        News.objects.create(subject=subject, message=message).setup(**kwargs)

    def create_scheduled_task(self):
        # create scheduled tast if scheduled_publish_date is set
        # ths work like newsletter.News.create_scheduled task, a placeholder task is create
        # and the hook is the one doign the real wok here using the slug of the post
        if self.status == Post.STATUS.published or not self.scheduled_publish_date:
            return
        try:
            Schedule.objects.create(
                func="blog.tasks.placeholder_task",
                name=f"{self.slug}",
                hook="blog.tasks.publish_post_hook",
                schedule_type=Schedule.ONCE,
                next_run=self.scheduled_publish_date,
            )
        except (ProgrammingError, IntegrityError, OperationalError):
            pass

    def save(self, *args, **kwargs):
        self.create_scheduled_task()
        super().save(*args, **kwargs)


# TODO Find a way to manipulate post order
class Series(Postable, StatusModel, TimeStampedModel, SoftDeletableModel):
    STATUS = Choices("in_progress", "on_break", "finished")
    status = StatusField(default=STATUS.in_progress)
    status_changed = MonitorField(monitor="status")

    class Meta:
        verbose_name_plural = "series"

    def get_absolute_url(self):
        return reverse("blog:series_detail", kwargs={"slug": self.slug})

    def all_blogpost(self):
        return Post.objects.filter(series=self).order_by("created")

    @property
    def categories(self):
        categories = Category.objects.none()
        posts = self.all_blogpost()
        for post in posts:
            categories = Category.objects.filter(
                Q(id__in=post.categories.all()) | Q(id__in=categories)
            )
        return categories

    @property
    def reading_time(self):
        all_posts = self.all_blogpost()
        return all_posts.aggregate(Sum("reading_time")).get("reading_time__sum")
