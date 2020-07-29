from django.urls import path
from .views import UserRegisterView

app_name = 'members'
urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
]