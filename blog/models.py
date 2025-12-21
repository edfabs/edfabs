from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField


STATUS = (
    (0, "Draft"),
    (1, "Publish"),
)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", args=(self.slug,))


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:tag", args=(self.slug,))


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    pinterest_url = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("blog:index")


class Post(models.Model):
    DRAFT = 0
    PUBLISHED = 1

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    content = RichTextField(blank=True, null=True)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/header_post/")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    status = models.IntegerField(choices=STATUS, default=DRAFT)
    created_on = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(blank=True, null=True)
    updated_on = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name="blog_posts", blank=True)

    class Meta:
        ordering = ["-published_at", "-created_on"]

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + "  |  " + str(self.author)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        if not self.meta_title:
            self.meta_title = self.title[:255]
        if not self.excerpt and self.content:
            self.excerpt = str(self.content)[:240]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", args=(self.slug,))


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s" % (self.post.title, self.name)
