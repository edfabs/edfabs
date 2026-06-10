from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import SetPasswordForm

User = get_user_model()

_WIDGET_TEXT = lambda extra=None: forms.TextInput(attrs={'class': 'form-control', **(extra or {})})
_WIDGET_EMAIL = lambda extra=None: forms.EmailInput(attrs={'class': 'form-control', **(extra or {})})
_WIDGET_PWD = lambda: forms.PasswordInput(attrs={'class': 'form-control'})


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=_WIDGET_EMAIL({'autocomplete': 'email'}),
    )
    full_name = forms.CharField(
        max_length=200,
        label='Nombre completo',
        widget=_WIDGET_TEXT(),
    )
    password = forms.CharField(
        min_length=8,
        label='Contraseña',
        widget=_WIDGET_PWD(),
    )
    password_confirm = forms.CharField(
        label='Confirmar contraseña',
        widget=_WIDGET_PWD(),
    )

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo ya está registrado.')
        return email

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password')
        p2 = cleaned.get('password_confirm')
        if p1 and p2 and p1 != p2:
            self.add_error('password_confirm', 'Las contraseñas no coinciden.')
        return cleaned


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=_WIDGET_EMAIL({'autofocus': True, 'autocomplete': 'email'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=_WIDGET_PWD(),
    )

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self._user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('email', '').lower().strip()
        password = cleaned.get('password')
        if email and password:
            self._user = authenticate(self.request, username=email, password=password)
            if self._user is None:
                raise forms.ValidationError('Correo o contraseña incorrectos.')
            if not self._user.is_active:
                raise forms.ValidationError('Esta cuenta está desactivada.')
        return cleaned

    def get_user(self):
        return self._user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['full_name', 'avatar']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'full_name': 'Nombre completo',
            'avatar': 'Foto de perfil',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'content_type'):
            if not avatar.content_type.startswith('image/'):
                raise forms.ValidationError('Solo se permiten archivos de imagen.')
        return avatar


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(
        label='Nuevo correo electrónico',
        widget=_WIDGET_EMAIL(),
    )
    password = forms.CharField(
        label='Contraseña actual',
        widget=_WIDGET_PWD(),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_email(self):
        email = self.cleaned_data['new_email'].lower().strip()
        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Este correo ya está en uso.')
        return email

    def clean_password(self):
        pwd = self.cleaned_data['password']
        if not self.user.check_password(pwd):
            raise forms.ValidationError('Contraseña incorrecta.')
        return pwd
