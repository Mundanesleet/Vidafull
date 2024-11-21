# citas/serializers.py

from rest_framework import serializers
from .models import Direccion

class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = ['id', 'direccion']
