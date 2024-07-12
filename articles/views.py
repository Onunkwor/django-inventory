from django.shortcuts import render
from articles.models import Article
# Create your views here.


def article_detail_view(request, id=None):
    object = None
    if id is not None:
        object = Article.objects.get(id=id)
    context = {
        'object': object
    }
    return render(request, 'articles/details.html', context=context)
