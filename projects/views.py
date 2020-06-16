from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from PIL import Image
import pytesseract
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def index(request):
	#return HttpResponse("Hello, world. You're at te skeleton index")
	return render(request, 'projects/index.html', {'title': 'Projects'})

def tesseract(request):
	#print(pytesseract.image_to_string(Image.open('Escanear.jpg')))
	#result = pytesseract.image_to_osd(Image.open(os.path.join(BASE_DIR, 'static/images/Escanear.jpeg')), config='--oem 3 --psm 6')
	#print(pytesseract.image_to_string(Image.open(os.path.join(BASE_DIR, 'static/images/Escanear.jpeg'))))
	#custom_oem_psm_config = r'--oem 3 --psm 6'
	#result = pytesseract.image_to_osd(Image.open(os.path.join(BASE_DIR, 'static/images/Escanear.jpeg')))
	result = pytesseract.image_to_pdf_or_hocr(Image.open(os.path.join(BASE_DIR, 'static/images/Escanear.jpeg')), extension='hocr')
	#result = result.replace('\n', '&nbsp')
	return HttpResponse("result: {}".format(result))
	#return render(request, 'projects/index.html', {"result: {}".format(result)})