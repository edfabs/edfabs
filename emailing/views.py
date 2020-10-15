from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
# Create your views here.

def index(request):

	return HttpResponse("Hello, world. You're at te skeleton index")
	#return render(request, 'skeleton/index.html', {'title': 'Home'})

#DataFlair #Send Email
def send(request):
    subject = 'Welcome to DataFlair'
    message = 'Hope you are enjoying your Django Tutorials'
    recepient = str('fabian.suchett@edfabs.com')
    send_mail(subject, message, EMAIL_HOST_USER, [recepient], fail_silently = False)
    # return render(request, 'subscribe/index.html', {'form':sub})
    return HttpResponse("Se envío el correo")
