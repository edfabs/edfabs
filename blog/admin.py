from django.contrib import admin
from .models import Post, Category
# from .models import Post

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)