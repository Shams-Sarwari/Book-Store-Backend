from django.db import models
from accounts.models import Profile


# Create your models here.
class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    read_by_admin = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    alt_text = models.CharField(max_length=100, blank=True, null=True)
    url = models.ImageField(upload_to="blog_images")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_images")

    def __str__(self) -> str:
        return f"image for {self.post}"


class Review(models.Model):
    comment = models.TextField(blank=True, null=True)
    rate = models.PositiveSmallIntegerField(default=1)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="post_reivews"
    )
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return f"comment from {self.profile}"


class Reply(models.Model):
    comment = models.TextField()
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="post_replies"
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name="post_replies"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        indexes = [models.Index(fields=["-created"])]

    def __str__(self) -> str:
        return f"reply from {self.profile}"
