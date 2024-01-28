from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
