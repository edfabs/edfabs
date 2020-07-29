from django import forms
from .models import Post
# from .models import Post, Category

# choices = Category.objects.all().values_list('name', 'name')

# choice_list = []

# for item in choices:
    # choice_list.append(item)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = ('title', 'slug', 'author', 'category', 'content')
        fields = ('title', 'slug', 'author', 'content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'choices' }),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            # 'category': forms.Select(choices=choice_list, attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug', 'content')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titulo de Post'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            #'author': forms.Select(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }