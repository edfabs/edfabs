from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
	#return HttpResponse("Hello, world. You're at te skeleton index")
	return render(request, 'skeleton/index.html', {'title': 'home'})