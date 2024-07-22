from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save
# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publish = models.DateField(
        auto_now=False, auto_now_add=False, null=True, blank=True)
    # default=timezone.now

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


def slugify_instance_title(instance, save=False):
    slug = slugify(instance.title)
    instance.slug = slug
    if save:
        instance.save()
    return instance


def article_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    if instance.slug is None:
        slug = slugify_instance_title(instance)


pre_save.connect(article_pre_save, sender=Article)


def article_post_save(sender, instance, created, *args, **kwargs):
    print('post_save')
    if created:
        slug = slugify_instance_title(instance)


post_save.connect(article_post_save, sender=Article)
