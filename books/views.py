from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import *
from .permissions import AdminOrOwnerReview
from .serializers import *
from .utils import paginate_items, search_items

import uuid


# Create your views here.
@api_view(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        cateogories = Category.objects.all()
        cateogories = paginate_items(request, cateogories, 8)
        serialized_data = CategorySerializer(cateogories, many=True)
        return Response(serialized_data.data)
    if request.method == "POST":
        serialized_data = CategorySerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors)


# this view returns books for specific category
@api_view(["GET"])
def category_books(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    booklines = BookLine.objects.filter(book__category=category, add_to_page=True)
    serialized_data = BookLineSerializer(booklines, many=True)
    return Response(serialized_data.data)


@api_view()
def test(request):
    return Response({"message": "welcome"})


@api_view(["GET", "POST"])
def book_list(request):
    if request.method == "GET":
        queryset = Book.objects.all()
        serialized_data = BookSerializer(queryset, many=True)
        return Response(serialized_data.data)

    if request.method == "POST":
        serialized_data = BookSerializer(data=request.data)
        if serialized_data.is_valid():
            print(serialized_data.validated_data)
            author = get_object_or_404(
                Author, id=serialized_data.validated_data.get("author_id")
            )
            category = get_object_or_404(
                Category, id=serialized_data.validated_data.get("category")["id"]
            )
            slug = slugify(serialized_data.validated_data.get("title"))

            # check if the slug is already in the database if so make it unique
            slugs = Book.objects.values_list("slug", flat=True)

            # accuracy loop for slug to ensure its unique
            while True:
                if slug in slugs:
                    random_string = str(uuid.uuid4()).replace("-", "")
                    slug = f"{slug}-{random_string}"
                else:
                    break
            serialized_data.save(author=author, category=category, slug=slug)
            return Response({"message": "Book created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors)


@api_view(["GET", "POST"])
def bookline_list(request, book_id=None):
    if request.method == "GET":
        search = request.query_params.get("search", None)
        if search:
            related_books = search_items(search, Book.objects.all())
            queryset = BookLine.objects.filter(book__in=related_books, add_to_page=True)
        else:
            queryset = BookLine.objects.filter(add_to_page=True)
        result = 8
        query = request.query_params.get("query", None)
        if query:
            if query == "bestselling":
                queryset = queryset.filter(book__best_seller=True)
                result = 4
            elif query == "mostviewed":
                print("inside most")
                queryset = queryset.order_by("-num_of_views")
        queryset = paginate_items(request, queryset, result)
        serialized_data = BookLineSerializer(queryset, many=True)
        return Response(serialized_data.data)

    if request.method == "POST":
        if book_id:
            book = get_object_or_404(Book, id=book_id)
            serialized_data = BookLineDetailSerializer(data=request.data)
            if serialized_data.is_valid():
                serialized_data.save(book=book)
                return Response(
                    {"message": "Bookline created"}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(serialized_data.errors)
        else:
            return Response(
                {"error": "Please provide id of related book"},
                status=status.HTTP_400_BAD_REQUEST,
            )


@api_view(["GET"])
def bookline_detail(request, pk):
    queryset = get_object_or_404(BookLine, id=pk)
    if request.method == "GET":
        serialized_data = BookLineDetailSerializer(queryset)
        return Response(serialized_data.data)


@api_view(["GET"])
def related_books(request, pk):
    category = get_object_or_404(Category, id=pk)
    booklines = BookLine.objects.filter(
        Q(book__category=category) & Q(add_to_page=True)
    )
    if len(booklines) < 10:
        queryset = booklines
    else:
        queryset = booklines[0:10]

    serialized_data = BookLineSerializer(queryset, many=True)
    return Response(serialized_data.data)


@api_view(["GET"])
def related_booklines(request, pk):
    bookline = get_object_or_404(BookLine, id=pk)
    related_booklines = BookLine.objects.filter(book=bookline.book).exclude(
        id=bookline.id
    )

    serialized_data = BookLineSerializer(related_booklines, many=True)
    return Response(serialized_data.data)


@api_view(["GET", "POST"])
def book_reviews(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    if request.method == "GET":
        reviews = Review.objects.filter(book=book)
        serialized_data = ReviewSerializer(reviews, many=True)
        return Response(serialized_data.data)

    if request.method == "POST":
        serialized_data = ReviewSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save(profile=request.user.profile, book=book)
            return Response(
                {"message": "review created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serialized_data.errors)


@api_view(["PATCH", "DELETE"])
@permission_classes([AdminOrOwnerReview])
def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user.is_superuser or request.user.profile == review.profile:
        if request.method == "PATCH":
            comment = request.data.get("comment")
            if comment:
                review.comment = comment
                review.save()
                return Response(
                    {"message": "successully updated"}, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    {"error": "error occured"}, status=status.HTTP_400_BAD_REQUEST
                )

        if request.method == "DELETE":
            review.delete()
            return Response(
                {"message": "review deleted successfully"}, status=status.HTTP_200_OK
            )

    else:
        return Response(
            {"message": "You are not allowed to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )


@api_view(["GET", "POST"])
def replies(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "GET":
        queryset = review.replies.all()
        serialzied_data = ReplySerializer(queryset, many=True)
        return Response(serialzied_data.data)

    if request.method == "POST":
        serialzied_data = ReplySerializer(data=request.data)
        if serialzied_data.is_valid():
            serialzied_data.save(profile=request.user.profile, review=review)
            return Response(
                {"message": "Reply created"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(serialzied_data.errors)


@api_view(["DELETE", "PATCH"])
def reply(request, reply_id):
    reply = get_object_or_404(Reply, id=reply_id)
    if request.method == "DELETE":
        reply.delete()
        return Response({"message": "Reply deleted"}, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        comment = request.data.get("comment")
        if comment:
            reply.comment = comment
            reply.save()
            return Response(
                {"message": "Reply changed successfully"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"message": "Error occured"}, status=status.HTTP_400_BAD_REQUEST
            )
