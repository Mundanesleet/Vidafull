from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),             
    path('programar/', views.programar_cita, name='programar_cita'),  
    path('citas/', views.citas, name='citas'),  
]
