from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, PasswordChangingForm, ProfilePageForm
from blog.models import Profile
from django.conf import settings
import json
import os
import urllib

# Create your views here.

class CreateProfilePageview(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile_page.html'
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EdithProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'pinterest_url']
    success_url = reverse_lazy('blog:index')


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'
    
    def get_context_data(self, *args, **kwargs):
        # users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context


class PasswordsChangeViews(PasswordChangeView):
    form_class = PasswordChangingForm
    # from_class = PasswordChangeForm
    success_url = reverse_lazy('members:password_success')

def password_success(request):
    return render(request, 'registration/password_success.html', {})

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha'] = settings.GOOGLE_RECAPTCHA_WEB_SITE
        return context

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        if not recaptcha_response:
            form.add_error(None, 'Confirma que no eres un robot.')
            return self.form_invalid(form)

        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        try:
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
        except Exception:
            form.add_error(None, 'No se pudo validar reCAPTCHA. Intenta nuevamente.')
            return self.form_invalid(form)

        if not result.get('success'):
            form.add_error(None, 'Invalid reCAPTCHA. Please try again.')
            return self.form_invalid(form)

        return super().form_valid(form)

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('blog:index')

    def get_object(self):
        return self.request.user


class RecaptchaLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recaptcha'] = settings.GOOGLE_RECAPTCHA_WEB_SITE
        return context

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response')
        if not recaptcha_response:
            form.add_error(None, 'Confirma que no eres un robot.')
            return self.form_invalid(form)

        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req = urllib.request.Request(url, data=data)
        try:
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())
        except Exception:
            form.add_error(None, 'No se pudo validar reCAPTCHA. Intenta nuevamente.')
            return self.form_invalid(form)

        if not result.get('success'):
            form.add_error(None, 'Invalid reCAPTCHA. Please try again.')
            return self.form_invalid(form)

        return super().form_valid(form)
