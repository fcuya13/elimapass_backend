from rest_framework import serializers
from .models import *

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class TarjetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarjeta
        fields = '__all__'

class ParaderoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paradero
        fields = '__all__'

class RecargaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recarga
        fields = '__all__'

class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = '__all__'

class ParaderoRutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParaderoRuta
        fields = '__all__'

class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

class ViajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Viaje
        fields = '__all__'
