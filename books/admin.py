from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Image)
admin.site.register(BookLine)
admin.site.register(Review)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}