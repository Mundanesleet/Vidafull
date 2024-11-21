from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),             
    path('programar/', views.programar_cita, name='programar_cita'),  
    path('citas/', views.citas, name='citas'),  
    path('create-address/', views.create_address.as_view(), name='create_address'),  
    path('obtener_horas_disponibles/', views.obtener_horas_disponibles, name='obtener_horas_disponibles'),
]
