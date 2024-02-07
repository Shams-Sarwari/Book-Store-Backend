from books.utils import paginate_items
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import PostSerializer, ReviewSerializer, ReplySerializer

import uuid


# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == "GET":
        search_text = request.query_params.get("search")
        if search_text:
            queryset = Post.objects.annotate(
                search=SearchVector("title", "body")
            ).filter(search=search_text)
        else:
            queryset = Post.objects.all()
        queryset = paginate_items(request, queryset, 6)
        serialized_data = PostSerializer(queryset, many=True)
        return Response(serialized_data.data)
    if request.method == "POST":
        serialized_data = PostSerializer(data=request.data)
        if serialized_data.is_valid():
            slug = slugify(serialized_data.validated_data.get("title"))
            # check if the slug is already in the database if so make it unique
            slugs = Post.objects.values_list("slug", flat=True)
            while True:
                if slug in slugs:
                    random_string = str(uuid.uuid4()).replace("-", "")
                    slug = f"{slug}-{random_string}"
                else:
                    break
            serialized_data.save(profile=request.user.profile, slug=slug)
            return Response({"message": "Post added"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized_data.errors)


@api_view(["GET", "DELETE", "PATCH"])
def post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == "GET":
        serialized_data = PostSerializer(post)
        return Response(serialized_data.data)

    if request.method == "DELETE":
        post.delete()
        return Response({"message": "Post deleted"}, status=status.HTTP_200_OK)

    if request.method == "PATCH":
        title = request.data.get("title")
        body = request.data.get("body")

        if title:
            post.title = title

        if body:
            post.body = body

        post.save()
        return Response({"message": "Post changed"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def post_reviews(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == "GET":
        reviews = Review.objects.filter(post=post)
        serialized_data = ReviewSerializer(reviews, many=True)
        return Response(serialized_data.data)

    if request.method == "POST":
        serialized_data = ReviewSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save(profile=request.user.profile, post=post)
            return Response(
                {"message": "review created successfully"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serialized_data.errors)


@api_view(["PATCH", "DELETE"])
def review_detail(request, review_id):
    review = get_object_or_404(Review, id=review_id)
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


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def replies(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "GET":
        queryset = review.post_replies.all()
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
