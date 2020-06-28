from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from markdownx.models import MarkdownxField
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel

from .utils import queryset_index_of

User = get_user_model()


# TODO need a monitor field to save the first time a blog is published
# TODO schedule a date to publish the post
# TODO default thumbnail for blog and projects


class Blogable(models.Model):
    thumbnail = models.ImageField(blank=True)
    title = models.CharField(max_length=150)
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:blogpost_list", kwargs={"category": self.name})


class BlogPost(Blogable, StatusModel, TimeStampedModel, SoftDeletableModel):
    STATUS = Choices("draft", "published")
    status = StatusField(default=STATUS.draft)
    status_changed = MonitorField(monitor="status")
    categories = models.ManyToManyField(Category)
    publish_date = models.DateTimeField(null=True, blank=True)
    scheduled_publish_date = models.DateTimeField(null=True, blank=True)
    blogpostseries = models.ForeignKey(
        "blog.BlogPostSeries", null=True, blank=True, on_delete=models.SET_NULL
    )

    def get_absolute_url(self):
        return reverse("blog:blogpost_detail", kwargs={"slug": self.slug})

    @property
    def is_published(self):
        return self.status == BlogPost.STATUS.published

    @property
    def published_on(self):
        if self.is_published:
            return self.status_changed

    @property
    def next_post(self):
        if not self.blogpostseries:
            return None
        blogposts = self.blogpostseries.all_blogpost()
        if self == blogposts.last():
            return None
        return blogposts[queryset_index_of(blogposts, self) + 1]

    @property
    def previous_post(self):
        if not self.blogpostseries:
            return None
        blogposts = self.blogpostseries.all_blogpost()
        if self == blogposts.first():
            return None
        return blogposts[queryset_index_of(blogposts, self) - 1]

    def belongs_to_series(self, blogpostseries):
        return self.blogpostseries == blogpostseries

    def publish(self):
        # set publication date
        pass


class BlogPostSeries(Blogable, StatusModel, TimeStampedModel, SoftDeletableModel):
    STATUS = Choices("in_progress", "on_break", "finished")
    status = StatusField(default=STATUS.in_progress)
    status_changed = MonitorField(monitor="status")

    def get_absolute_url(self):
        return reverse("blog:blogpostseries_detail", kwargs={"slug": self.slug})

    def all_blogpost(self):
        return BlogPost.objects.filter(blogpostseries=self).order_by("created")

    @property
    def categories(self):
        categories = Category.objects.none()
        blogposts = self.all_blogpost()
        for blogpost in blogposts:
            categories = Category.objects.filter(
                id__in=blogpost.categories.all() & Q(id__in=categories)
            )
        return categories


class Comment(TimeStampedModel):
    user_name = models.CharField(max_length=30)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
