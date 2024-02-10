from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


def search_items(search_text, queryset):
    # the SearchVector allows you to search in multiple attribiutes
    search_vector = SearchVector("title", weight="A") + SearchVector("body", weight="B")
    # the SearchQuery class does the stemming
    search_query = SearchQuery(search_text)
    queryset = (
        queryset.annotate(
            # SearchRank function orders the result on
            # how often the query appears and how close together they are
            search=search_vector,
            rank=SearchRank(search_vector, search_query),
        )
        .filter(rank__gte=0.2)
        .order_by("-rank")
    )
    return queryset
