from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Review)
admin.site.register(Image)
admin.site.register(Reply)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
