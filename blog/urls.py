from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('article/edit/<int:pk>',views.UpdatePostView.as_view(), name='update_post'),
]