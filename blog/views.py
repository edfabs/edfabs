from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.text import slugify
from django.db.models import F
from .models import Post, Category, Comment, Tag
from .forms import PostForm, EditForm, CategoryForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

# Create your views here.



def LikeView(request, slug):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    post = get_object_or_404(Post, slug=slug)
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('blog:detail', args=[post.slug]))

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'latest_post_list'
    paginate_by = 9
    queryset = Post.objects.filter(status=Post.PUBLISHED).select_related("category", "author").prefetch_related("tags")

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        tag_menu = Tag.objects.all()
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        context["tag_menu"] = tag_menu
        return context

def CategoryView(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category_posts = Post.objects.filter(category=category, status=Post.PUBLISHED).select_related("category", "author").prefetch_related("tags")
    return render(request, 'blog/categories.html', {
        'category': category,
        'category_posts': category_posts,
        'cat_menu': Category.objects.all(),
    })


def TagView(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    tag_posts = tag.posts.filter(status=Post.PUBLISHED).select_related("category", "author").prefetch_related("tags")
    return render(request, 'blog/tags.html', {
        'tag': tag,
        'tag_posts': tag_posts,
        'cat_menu': Category.objects.all(),
    })

class DetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        qs = super().get_queryset().select_related("category", "author").prefetch_related("tags", "comments")
        if self.request.user.is_authenticated and (self.request.user.is_staff or self.request.user.is_superuser):
            return qs
        return qs.filter(status=Post.PUBLISHED)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # increment views count
        Post.objects.filter(pk=obj.pk).update(views_count=F("views_count") + 1)
        obj.refresh_from_db(fields=["views_count"])
        return obj
    
    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        stuff = self.object
        total_likes = stuff.total_likes()

        liked = False
        if self.request.user.is_authenticated and stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["cat_menu"] = cat_menu
        # simple related posts by category
        related = Post.objects.filter(category=stuff.category, status=Post.PUBLISHED).exclude(pk=stuff.pk)[:3]

        context["liked"] = liked
        context["total_likes"] = total_likes
        context["related_posts"] = related
        return context
    
class AddPostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('blog:index')

    def form_valid(self, form):
        if not form.instance.slug:
            form.instance.slug = slugify(form.instance.title)
        form.instance.author = self.request.user
        return super().form_valid(form)

class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'
    # fields = '__all__'
    def form_valid(self, form):
        slug = self.kwargs.get("slug")
        if slug:
            post = get_object_or_404(Post, slug=slug)
            form.instance.post = post
        else:
            form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('blog:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_slug = self.kwargs.get("slug")
        post_pk = self.kwargs.get("pk")
        context["post_id"] = post_pk
        if post_slug:
            context["post_slug"] = post_slug
        elif post_pk:
            try:
                context["post_slug"] = Post.objects.only("slug").get(pk=post_pk).slug
            except Post.DoesNotExist:
                context["post_slug"] = None
        return context

    def get_success_url(self):
        return reverse_lazy("blog:detail", args=[self.object.post.slug])


class AddCategoryView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'blog/add_category.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

class UpdatePostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'blog/update_post.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    form_class = EditForm
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:index')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
