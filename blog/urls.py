from django.urls import path
from . import views
from .views import CategoryView, LikeView, TagView

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<slug:slug>/', views.DetailView.as_view(), name='detail'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),    
    path('article/edit/<int:pk>',views.UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/remove',views.DeletePostView.as_view(), name='delete_post'),
    path('categoria/<slug:slug>/', CategoryView, name='category'),
    path('tag/<slug:slug>/', TagView, name='tag'),
    path('like/<slug:slug>/', LikeView, name='like_post'),
    path('post/<slug:slug>/comment/', views.AddCommentView.as_view(), name='add_comment'),
    path('article/<int:pk>/comment/', views.AddCommentView.as_view(), name='add_comment_legacy'),
]
