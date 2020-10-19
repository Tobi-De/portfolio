from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.db import models, IntegrityError, ProgrammingError, OperationalError
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from django_extensions.db.fields import AutoSlugField, RandomCharField
from django_q.tasks import Schedule, schedule
from markdownx.models import MarkdownxField
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel

from core.templatetags.core_tags import markdown
from core.utils import get_current_domain_url
from newsletter.models import News

User = get_user_model()


# TODO autosave content and revert changes and ctrl + s to save
class Postable(models.Model):
    thumbnail = models.OneToOneField(
        "core.Thumbnail", blank=True, null=True, on_delete=models.SET_NULL
    )
    title = models.CharField(max_length=150)
    overview = MarkdownxField()
    body = MarkdownxField(blank=True)
    slug = AutoSlugField(populate_from=["title"])

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
    publish_date = models.DateTimeField(null=True, blank=True)
    scheduled_publish_date = models.DateTimeField(null=True, blank=True)
    series = models.ForeignKey(
        "blog.Series", null=True, blank=True, on_delete=models.SET_NULL
    )
    featured = models.BooleanField(default=False)
    secret_key = RandomCharField(length=64)

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    @property
    def is_published(self):
        return self.status == Post.STATUS.published

    @property
    def next_post(self):
        if not self.series:
            return None
        posts = self.series.all_published_post()
        if self == posts.last() or self not in posts:
            return None
        return posts[list(posts).index(self) + 1]

    @property
    def previous_post(self):
        if not self.series:
            return None
        posts = self.series.all_published_post()
        if self == posts.first() or self not in posts:
            return None
        return posts[list(posts).index(self) - 1]

    def publish(self):
        self.status = Post.STATUS.published
        self.publish_date = timezone.now()
        self.save()
        self.send_publish_email()

    def send_publish_email(self):
        # send email to subscribers to inform of new post
        subject = "New Post!"
        message = render_to_string(
            "blog/email/new_post_message.html",
            context={
                "title": self.title,
                "link": f"{get_current_domain_url()}{self.get_absolute_url()}",
            },
        ).format("utf-8")
        News.objects.create(subject=subject, message=message).setup()

    def create_scheduled_task(self):
        # create scheduled tast if scheduled_publish_date is set
        # ths work like newsletter.News.create_scheduled task, a placeholder task is create
        # and the hook is the one doign the real wok here using the slug of the post
        if self.is_published or not self.scheduled_publish_date:
            return
        try:
            schedule(
                func="blog.tasks.publish_post_task",
                slug=self.slug,
                schedule_type=Schedule.ONCE,
                next_run=self.scheduled_publish_date,
            )
        except (ProgrammingError, IntegrityError, OperationalError):
            pass

    def save(self, *args, **kwargs):
        self.create_scheduled_task()
        super().save(*args, **kwargs)

    @property
    def sharable_url(self):
        """
        An url to reach this post (there is a secret url for sharing unpublished
        posts to outside users).
        """
        if not self.is_published:
            return reverse(
                "blog:secret_post_detail", kwargs={"secret_key": self.secret_key}
            )
        else:
            return self.get_absolute_url()

    @property
    def reading_time(self):
        word_count = len(strip_tags(markdown(self.body)).split())
        minutes = int(str(word_count / 200).split(".")[0])
        seconds = round(int(str(word_count / 200).split(".")[1]) * 0.60)
        return minutes if seconds < 30 else (minutes + 1)

    @classmethod
    def all_published_post(cls):
        return Post.objects.filter(status=Post.STATUS.published).order_by(
            "-publish_date"
        )


class Series(Postable, StatusModel, TimeStampedModel, SoftDeletableModel):
    STATUS = Choices("in_progress", "on_break", "finished")
    status = StatusField(default=STATUS.in_progress)
    status_changed = MonitorField(monitor="status")
    visible = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "series"

    def get_absolute_url(self):
        return reverse("blog:series_detail", kwargs={"slug": self.slug})

    def all_published_post(self):
        return Post.objects.filter(series=self, status=Post.STATUS.published).order_by(
            "publish_date"
        )

    @property
    def categories(self):
        categories = Category.objects.none()
        posts = self.all_published_post()
        for post in posts:
            categories = Category.objects.filter(
                Q(id__in=post.categories.all()) | Q(id__in=categories)
            )
        return categories

    @property
    def reading_time(self):
        all_posts_reading_time = [
            post.reading_time for post in self.all_published_post()
        ]
        return sum(all_posts_reading_time)
