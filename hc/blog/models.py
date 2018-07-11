from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.models import User


class Category(models.Model):
    owner = models.ForeignKey(
        User, related_name='categories', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class PublishedManager(models.Manager):
    def get_queryset(self):
        today = timezone.now()
        return super(PublishedManager, self).get_queryset().filter(
            status='published').filter(Q(publish__lte=today))


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=125)
    author = models.ForeignKey(
        User, related_name='blog_posts', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="posts", on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    publish = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='draft')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-publish',)

    def get_view_absolute_url(self):
        return reverse("hc-view-post", args=[self.publish.year,
                                             self.publish.strftime('%m'),
                                             self.publish.strftime('%d'),
                                             self.slug])

    objects = models.Manager()
    published = PublishedManager()


class Comment(models.Model):
    post = models.ForeignKey(
        Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
