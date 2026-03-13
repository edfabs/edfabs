from django.urls import path

from . import views

app_name = 'skeleton'
urlpatterns = [
	path('', views.index, name='index'),
	path(
		'RefineriaTula50Aniversario/',
		views.refineria_tula_50_aniversario,
		name='refineria_tula_50_aniversario',
	),
	path('articles/', views.articles, name='articles'),
	path('about/', views.about, name='about'),
	path('contact/', views.contact, name='contact'),
	path('privacidad/', views.privacidad, name='privacidad'),
	path('terminos/', views.terminos, name='terminos'),
	path('servicios/', views.servicios, name='servicios')
]
