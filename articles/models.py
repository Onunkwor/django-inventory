from django.db import models
from django.db.models.signals import pre_save, post_save
from articles.utils import slugify_instance_title
from django.urls import reverse
from django.db.models import Q
# Create your models here.


class ArticleQuerySet(models.QuerySet):
    def search(self, query):
        if query is None or query == '':
            return self.none()
        lookups = Q(title__icontains=query) | Q(content__icontains=query) | Q()
        return self.filter(lookups)


class ArticleManager(models.Manager):

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    # default=timezone.now
    objects = ArticleManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # return f'/articles/{self.slug}'
        return reverse('article-detail', kwargs={'slug': self.slug})


def article_pre_save(sender, instance, *args, **kwargs):
    if instance.slug is None:
        slug = slugify_instance_title(instance)


pre_save.connect(article_pre_save, sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    if created:
        slug = slugify_instance_title(instance, save=True)


post_save.connect(article_post_save, sender=Article)
