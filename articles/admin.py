from django.contrib import admin
from .models import Article
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'slug', 'timestamp', 'updated']
    search_fields = ['title', 'content']


admin.site.register(Article, ArticleAdmin)
