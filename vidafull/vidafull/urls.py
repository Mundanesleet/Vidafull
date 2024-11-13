from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('citas/', include('citas.urls')),  # Ruta para la aplicación citas
]