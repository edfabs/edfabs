from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from PIL import Image
import pytesseract

def index(request):
	#return HttpResponse("Hello, world. You're at te skeleton index")
	return render(request, 'projects/index.html', {'title': 'Projects'})

def tesseract(request):
	print(pytesseract.image_to_string(Image.open('Escanear.jpg')))