from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

# Create your models here.

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        #return reverse('blog:detail', args=(str(self.id)))
        return reverse('blog:index')

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE) 
    bio = models.TextField()
    profile_pic = models.ImageField(null=True,blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=200, null=True, blank=True)
    facebook_url = models.CharField(max_length=200, null=True, blank=True)
    twitter_url = models.CharField(max_length=200, null=True, blank=True)
    instagram_url = models.CharField(max_length=200, null=True, blank=True)
    pinterest_url = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.user)
    
    def get_absolute_url(self):
        #return reverse('blog:detail', args=(str(self.id)))
        return reverse('blog:index')


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    header_image = models.ImageField(null=True,blank=True, upload_to="images/header_post/")
    slug = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_post')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextField(blank=True, null=True)
    # content =
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    snippet = models.CharField(max_length=255, default="Click Link Above To Read Blog Post...")
    likes = models.ManyToManyField(User, related_name='blog_posts')

    class Meta:
        ordering = ['-created_on']

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title + '  |  ' + str(self.author)

    def get_absolute_url(self):
        #return reverse('blog:detail', args=(str(self.id)))
        return reverse('blog:index')