from django.views.generic import ListView, DetailView
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    queryset = Project.objects.filter(is_active=True).order_by("order", "-created_at")


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
