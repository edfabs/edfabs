from django.shortcuts import render
from django.views import generic
from .models import Post

# Create your views here.

class IndexView(generic.ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'

class DetailView(generic.DetailView):
    model = Post
    template_name = 'blog/detail.html'