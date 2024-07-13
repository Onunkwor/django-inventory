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


def article_search_view(request):
    # print(request.user)
    query_dict = dict(request.GET)
    query = query_dict.get('q')
    object_list = None

    if query and len(query) > 0:
        try:
            # Attempt to convert the query to an integer
            query_id = int(query[0])
            # If successful, try to find an article by ID
            object_list = [Article.objects.get(id=query_id)]
        except ValueError:
            # If conversion fails, assume the query is a string
            query_string = query[0]
            # Search for articles containing the query string in their title
            object_list = Article.objects.filter(title__icontains=query_string)
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
def article_create_view(request):
    context = {}
    if request.method == 'POST':
        title, content = request.POST.get('title'), request.POST.get('content')
        object = Article.objects.create(title=title, content=content)
        if title and object:
            context['title'] = title
            context['content'] = content
            context['created'] = True
            context['object'] = object
        else:
            context['created'] = False
    else:
        context['created'] = False
    return render(request, 'articles/create.html', context=context)
