from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, Sum
from django.urls import reverse
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField
from markdownx.models import MarkdownxField
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel

from .utils import queryset_index_of

User = get_user_model()


# TODO schedule a date to publish the post
# TODO default thumbnail for blog and projects


class Postable(models.Model):
    thumbnail = models.ImageField(upload_to='blog', blank=True)
    title = models.CharField(max_length=150)
    overview = models.TextField(max_length=200)
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
        return Post.objects.filter(categories__name=self.name, status=Post.STATUS.published).count()


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

    def publish(self):
        self.status = Post.STATUS.published
        self.publish_date = timezone.now()
        self.save()

    @classmethod
    def popular_posts(cls):
        # posts_with_comment = Post.objects.filter(status=Post.STATUS.published).annotate(comment_nums=Count("comment"))
        # try:
        #     first = second = third = posts_with_comment[0]
        # except IndexError:
        #     return []
        # for post in posts_with_comment:
        #     if post.comment_nums > first.comment_nums:
        #         first, second, third = post, first, second
        #     elif post.comment_nums > second.comment_nums:
        #         second, third = post, second
        #     elif post.comment_nums > third.comment_nums:
        #         third = post
        # return {first, second, third}
        return Post.objects.all()


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
