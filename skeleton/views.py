from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import Contacto

from django.core.mail import BadHeaderError, send_mail
from django.contrib import messages

from django.conf import settings
import os

import json
import urllib

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
			
			''' Begin reCAPTCHA validation '''
			recaptcha_response = request.POST.get('g-recaptcha-response')
			url = 'https://www.google.com/recaptcha/api/siteverify'
			values = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
			data = urllib.parse.urlencode(values).encode()
			req =  urllib.request.Request(url, data=data)
			response = urllib.request.urlopen(req)
			result = json.loads(response.read().decode())
			''' End reCAPTCHA validation '''

			if result['success']:
				try:
					send_mail(subject, name+' envío el siguiente mensaje'+message+' de '+sender, 'fabian.suchett@edfabs.com', ['fabian.suchett@edfabs.com'])
				except BadHeaderError:
					return HttpResponse('Invalid header found.')
				messages.success(request, 'mensaje enviado.')
				return HttpResponseRedirect('/contact/')
			else:
				messages.error(request, 'Invalid reCAPTCHA. Please try again.')
				return HttpResponseRedirect('/contact/')
		else:
			messages.error(request, 'hay un problema.')
			return HttpResponseRedirect('/contact/')
	else:
		form = Contacto()
		recaptcha = os.getenv("GOOGLE_RECAPTCHA_WEB_SITE")
		context = {'form': form, 'recaptcha': recaptcha}
	return render(request, 'skeleton/contact.html', context)