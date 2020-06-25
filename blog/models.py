import environ
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from markdownx.models import MarkdownxField
from model_utils import Choices
from model_utils.fields import MonitorField, StatusField
from model_utils.models import TimeStampedModel, SoftDeletableModel, StatusModel

env = environ.Env()
app_root_url = env("APP_ROOT_URL", default="http://0.0.0.0/")

from .exceptions import AuthorDoesNotMatchError

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
    slug = AutoSlugField(populate_from=["name"])
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:blogpost_list", kwargs={"category": self.slug})


class Comment(TimeStampedModel, SoftDeletableModel):
    author = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    content = models.TextField()
    blogpost = models.ForeignKey("blog.BlogPost", on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class BlogPost(Blogable, StatusModel, TimeStampedModel, SoftDeletableModel):
    STATUS = Choices("draft", "published")
    status = StatusField(default=STATUS.draft)
    status_changed = MonitorField(monitor="status")
    categories = models.ManyToManyField(Category)
    blogpostseries = models.ForeignKey(
        "blog.BlogPostSeries", null=True, blank=True, on_delete=models.SET_NULL
    )

    def get_absolute_url(self):
        return reverse(f"blog:blogpost_detail", kwargs={"slug": self.slug})

    @property
    def is_published(self):
        return self.status == BlogPost.STATUS.published

    @property
    def published_on(self):
        if self.is_published:
            return self.status_changed

    def belongs_to_series(self, blogpostseries):
        return self.blogpostseries == blogpostseries

    def publish(self):
        pass


class BlogPostSeries(Blogable, StatusModel, TimeStampedModel, SoftDeletableModel):
    STATUS = Choices("in_progress", "on_break", "finished")
    status = StatusField(default=STATUS.in_progress)
    status_changed = MonitorField(monitor="status")

    def get_absolute_url(self):
        return reverse(f"blog:blogpostseries_detail", kwargs={"slug": self.slug})

    def auto_generated_body(self):
        if not self.body:
            self.body = f"##{self.title.upper()} Series\n\n###Blog post include\n\n"
            self.save()

    def add_blogpost(self, blogpost):
        if blogpost.author != self.author:
            raise AuthorDoesNotMatchError
        blogpost.blogpostseries = self
        blogpost.save()
        lenght = len(list(self.as_generator()))
        self.body += f"{lenght + 1}. [{blogpost.title}]({app_root_url}{blogpost.get_absolute_url()})\n"
        self.save()

    def delete_blogpost(self, blogpost):
        if blogpost.belongs_to_series(blogpostseries=self):
            blogpost.blogpostseries = None
            blogpost.save()

    def as_generator(self):
        # return a generator fo all blogpost of this series
        for blogpost in BlogPost.objects.all():
            if blogpost.blogpostseries == self:
                yield blogpost

    @property
    def categories(self):
        categories = Category.objects.none()
        blogposts = self.as_generator()
        for blogpost in blogposts:
            categories = Category.objects.filter(
                id__in=blogpost.categories.all() & Q(id__in=categories)
            )
        return categories
