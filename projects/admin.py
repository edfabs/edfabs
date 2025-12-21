from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "order", "created_at")
    list_filter = ("is_active",)
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("is_active", "order")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("order", "-created_at")
