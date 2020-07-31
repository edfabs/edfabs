from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category
from .forms import PostForm, EditForm, CategoryForm
from django.urls import reverse_lazy

# Create your views here.

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'
    #ordering = ['-id']
    cats = Category.objects.all()

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category__name=cats.replace('-',' '))
    return render(request, 'blog/categories.html', {'cats': cats.title().replace('-',' '), 'category_posts': category_posts})

class DetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    # fields = '__all__'

class AddCategoryView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/add_category.html'
    #fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/update_post.html'
    #fields = ['title', 'slug', 'content']

class DeletePostView(DeleteView):
    model = Post
    form_class = EditForm
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:index')
