from django import forms
from .models import Post, Category, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'slug',
            'category',
            'tags',
            'status',
            'excerpt',
            'content',
            'header_image',
            'meta_title',
            'meta_description',
        )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título del artículo' }),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'slug-seo-friendly'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meta title'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'slug',
            'category',
            'tags',
            'status',
            'excerpt',
            'content',
            'header_image',
            'meta_title',
            'meta_description',
        )

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo de Post'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'meta_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Meta title'}),
            'meta_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name', 'slug', 'description',)

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de categoría'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'slug-de-categoria'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Descripción corta'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body', )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }
