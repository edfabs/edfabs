from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django import forms
from blog.models import Profile

User = get_user_model()

_FC = {'class': 'form-control'}


class ProfilePageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'website_url', 'facebook_url',
                  'twitter_url', 'instagram_url', 'pinterest_url')
        widgets = {
            'bio': forms.Textarea(attrs=_FC),
            'website_url': forms.TextInput(attrs=_FC),
            'facebook_url': forms.TextInput(attrs=_FC),
            'twitter_url': forms.TextInput(attrs=_FC),
            'instagram_url': forms.TextInput(attrs=_FC),
            'pinterest_url': forms.TextInput(attrs=_FC),
        }


class SignUpForm(UserCreationForm):
    """Formulario de registro adaptado a CustomUser (email + full_name)."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs=_FC),
        label='Correo electrónico',
    )
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs=_FC),
        label='Nombre completo',
    )

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update(_FC)
        self.fields['password2'].widget.attrs.update(_FC)


class EditProfileForm(UserChangeForm):
    """Formulario de edición de perfil adaptado a CustomUser."""
    email = forms.EmailField(widget=forms.TextInput(attrs=_FC), label='Correo electrónico')
    full_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs=_FC), label='Nombre completo')
    last_login = forms.CharField(max_length=100, widget=forms.TextInput(attrs=_FC), required=False, label='Último login')
    is_superuser = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_staff = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_active = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    date_joined = forms.CharField(max_length=100, widget=forms.TextInput(attrs=_FC), required=False)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'password', 'last_login',
                  'is_superuser', 'is_staff', 'is_active', 'date_joined')


class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={**_FC, 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={**_FC, 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={**_FC, 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')
