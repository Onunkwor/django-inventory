from django.http import HttpResponse
from articles.models import Article
from django.template.loader import render_to_string


def home_view(request):
    article_obj = Article.objects.get(id=4)
    article_qs = Article.objects.all()
    context = {
        'object_list': article_qs,
        "title":  article_obj.title,
        "content": article_obj.content
    }

    HTML_STRING = render_to_string('home-view.html', context=context)
    return HttpResponse(HTML_STRING)
