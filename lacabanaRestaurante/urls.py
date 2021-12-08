from django.urls import path
from . import views


app_name = "lacabanaRestaurante"
urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("pizza", views.pizza, name="pizza"),
    path("antojo", views.antojo, name="antojo"),
    path("cafe", views.cafe, name="cafe"),
    path("crepas", views.crepas, name="crepas"),
    path("alitas", views.alitas, name="alitas"),
]
