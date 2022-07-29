from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
	#return HttpResponse("Hello, world. You're at te skeleton index")
	return render(request, 'skeleton/index.html', {'title': 'Home'})

def articles(request):
	return render(request, 'skeleton/articles.html', {'title': 'Articles'})

def about(request):
	return render(request, 'skeleton/about.html', {'title': 'About'})

def contact(request):
	return render(request, 'skeleton/contact.html', {'title': 'Contact'})

def servicios(request):
	return render(request, 'skeleton/servicios.html', {'title': 'Servicios'})