from blogs.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def paginate_items(request, items, result):
    page = request.query_params.get("page", 1)
    paginator = Paginator(items, result)
    try:
        items = paginator.page(page)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        items = paginator.page(1)

    return items


def search_items(search_text):
    # the SearchVector allows you to search in multiple attribiutes
    search_vector = SearchVector("title", weight="A") + SearchVector("body", weight="B")
    # the SearchQuery class does the stemming
    search_query = SearchQuery(search_text)
    queryset = (
        Post.objects.annotate(
            # SearchRank function orders the result on
            # how often the query appears and how close together they are
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
        )
        .filter(rank__gte=0.2)
        .order_by("-rank")
    )
    return queryset
