from django.urls import path
from . import views
from .views import registrar_asistencia, index, upload_file

app_name = 'asambleas'
urlpatterns = [
    path('', index, name='index'),
    path('asamblea/<int:asamblea_id>/registrar/', registrar_asistencia, name='registrar_asistencia'),
    path('upload/', upload_file, name='upload_file'),
]