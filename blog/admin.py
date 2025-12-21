from django.contrib import admin
from .models import Post, Category, Profile, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "category", "published_at", "created_on")
    list_filter = ("status", "category", "author", "tags")
    search_fields = ("title", "content", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author",)
    filter_horizontal = ("tags", "likes")
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
    readonly_fields = ("views_count", "published_at", "updated_on", "created_on")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Profile)
admin.site.register(Comment)
