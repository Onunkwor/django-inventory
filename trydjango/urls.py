"""trydjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from articles import views as articles_views
from account import views as account_views
urlpatterns = [
    path('', views.home_view),
    path('recipes/', include('recipes.urls')),
    path('admin/', admin.site.urls),
    path('articles/', articles_views.article_search_view),
    path('articles/create/', articles_views.article_create_view,
         name='article-create'),
    path('articles/<str:slug>/',
         articles_views.article_detail_view, name='article-detail'),
    path('login/', account_views.login_view),
    path('logout/', account_views.logout_view),
    path('register/', account_views.register_view),

]
