from django.urls import path
from .views import UserRegisterView, UserEditView, PasswordsChangeViews, ShowProfilePageView, EdithProfilePageView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'members'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change_password.html')),
    path('password/', PasswordsChangeViews.as_view(template_name='registration/change_password.html')),
    path('password_success', views.password_success, name="password_success"),
    path('<int:pk>/profile', ShowProfilePageView.as_view(), name="show_profile_page"),
    path('<int:pk>/edit_profile_page', EdithProfilePageView.as_view(), name="edit_profile_page"),

]