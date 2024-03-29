from django.urls import path
from . import views
from .views import CategoryView, LikeView

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('article/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('add_category/', views.AddCategoryView.as_view(), name='add_category'),    
    path('article/edit/<int:pk>',views.UpdatePostView.as_view(), name='update_post'),
    path('article/<int:pk>/remove',views.DeletePostView.as_view(), name='delete_post'),
    path('category/<str:cats>/', CategoryView, name='category'),
    path('like/<int:pk>', LikeView, name='like_post'),
    path('article/<int:pk>/comment/', views.AddCommentView.as_view(), name='add_comment'),
]