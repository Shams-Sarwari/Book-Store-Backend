from books.utils import paginate_items
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import PostSerializer

import uuid


# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def posts(request):
    if request.method == "GET":

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


@api_view(["GET", "DELETE"])
def post(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    if request.method == "GET":
        serialized_data = PostSerializer(post)
        return Response(serialized_data.data)

    if request.method == "DELETE":
        post.delete()
        return Response({"message": "Post deleted"}, status=status.HTTP_200_OK)
