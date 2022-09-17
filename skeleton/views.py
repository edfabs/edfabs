from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Contacto
import os
from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages

# Create your views here.

from django.http import HttpResponse

def index(request):
	#return HttpResponse("Hello, world. You're at te skeleton index")
	return render(request, 'skeleton/index.html', {'title': 'Home'})

def articles(request):
	return render(request, 'skeleton/articles.html', {'title': 'Articles'})

def about(request):
	return render(request, 'skeleton/about.html', {'title': 'About'})

# def contact(request):
# 	return render(request, 'skeleton/contact.html', {'title': 'Contact'})

def servicios(request):
	return render(request, 'skeleton/servicios.html', {'title': 'Servicios'})

def contact(request):
	if request.method == 'POST':
		form = Contacto(request.POST)
		if form.is_valid():
			name = request.POST.get('name')
			sender = request.POST.get('sender')
			message = request.POST.get('mensaje')
			subject = 'Mensaje del formulario de contacto de edfabs.com'
			try:
				send_mail(subject, name+' envío el siguiente mensaje'+message+' de '+sender, os.getenv("EMAIL_HOST_USER"), os.getenv("EMAIL_HOST_USER"))
			except BadHeaderError:
				return HttpResponse('Invalid header found.')
			messages.success(request, 'mensaje enviado.')
			return HttpResponseRedirect('/contact/')
		else:
			messages.error(request, 'hay un problema.')
			return HttpResponseRedirect('/contact/')
	else:
		form = Contacto()
	return render(request, 'skeleton/contact.html', {'form': form})