from django.shortcuts import render

# Create your views here.


def index(request):
    # return HttpResponse("Hello, world. You're at te skeleton index")
    return render(request, "lacabanaRestaurante/index.html", {"title": "lacabana"})


def menu(request):
    return HttpResponse(request)


def pizza(request):
    # return HttpResponse("Hello, world. You're at te skeleton index")
    return render(request, "lacabanaRestaurante/pizza.html", {"title": "lacabana"})


def antojo(request):
    # return HttpResponse("Hello, world. You're at te skeleton index")
    return render(request, "lacabanaRestaurante/antojo.html", {"title": "lacabana"})


def cafe(request):
    # return HttpResponse("Hello, world. You're at te skeleton index")
    return render(request, "lacabanaRestaurante/cafe.html", {"title": "lacabana"})


def crepas(request):
    # return HttpResponse("Hello, world. You're at te skeleton index")
    return render(request, "lacabanaRestaurante/crepas.html", {"title": "lacabana"})


def alitas(request):
    # return HttpResponse("Hello, world. You're at te skeleton index")
    return render(request, "lacabanaRestaurante/alitas.html", {"title": "lacabana"})
