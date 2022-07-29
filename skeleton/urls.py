from django.urls import path

from . import views

app_name = 'skeleton'
urlpatterns = [
	path('', views.index, name='index'),
	path('articles/', views.articles, name='articles'),
	path('about/', views.about, name='about'),
	path('contact/', views.contact, name='contact'),
	path('servicios/', views.servicios, name='servicios')
]