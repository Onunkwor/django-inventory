from django.shortcuts import render
from articles.models import Article
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
# Create your views here.


def article_detail_view(request, slug=None):
    object = None
    if slug is not None:
        try:
            object = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            return render(request, 'articles/404.html')
    context = {
        'object': object
    }
    return render(request, 'articles/details.html', context=context)


def article_search_view(request):
    # print(request.user)
    query_dict = dict(request.GET)
    query = query_dict.get('slug')
    object_list = None

    if query and len(query) > 0:
        try:
            # Attempt to convert the query to an integer
            query_id = str(query[0])
            # If successful, try to find an article by ID
            lookups = Q(id=query_id)
            object_list = list(Article.objects.get(lookups))
        except ValueError:
            # If conversion fails, assume the query is a string
            query_string = query[0]
            # Search for articles containing the query string in their title

            object_list = Article.objects.search(query=query_string)
        except Article.DoesNotExist:
            # Handle the case where no article with the given ID is found
            object_list = []
        except Exception as e:
            # Handle any other exceptions
            print(f"An unexpected error occurred: {e}")
            object_list = []

    context = {
        'object_list': object_list,
    }
    return render(request, 'articles/search.html', context=context)


# @csrf_exempt
@login_required
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {}
    # print(dir(form))
    if form.is_valid():
        # title, content = form.cleaned_data.get(
        #     'title'), form.cleaned_data.get('content')
        # object = Article.objects.create(title=title, content=content)
        object = form.save()
        if object:
            context['created'] = True
            context['object'] = object
        else:
            context['created'] = False
            form = ArticleForm()
    context['form'] = form
    return render(request, 'articles/create.html', context=context)
