from rest_framework import generics
from .models import Usuario, Tarjeta, Paradero, Recarga, Ruta, ParaderoRuta, Bus, Viaje
from .serializers import (
    UsuarioSerializer, TarjetaSerializer, ParaderoSerializer,
    RecargaSerializer, RutaSerializer, ParaderoRutaSerializer,
    BusSerializer, ViajeSerializer
)

class UsuarioList(generics.ListCreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class TarjetaList(generics.ListCreateAPIView):
    queryset = Tarjeta.objects.all()
    serializer_class = TarjetaSerializer

class TarjetaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarjeta.objects.all()
    serializer_class = TarjetaSerializer

class ParaderoList(generics.ListCreateAPIView):
    queryset = Paradero.objects.all()
    serializer_class = ParaderoSerializer

class ParaderoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Paradero.objects.all()
    serializer_class = ParaderoSerializer

class RecargaList(generics.ListCreateAPIView):
    queryset = Recarga.objects.all()
    serializer_class = RecargaSerializer

class RecargaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recarga.objects.all()
    serializer_class = RecargaSerializer

class RutaList(generics.ListCreateAPIView):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class RutaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

class ParaderoRutaList(generics.ListCreateAPIView):
    queryset = ParaderoRuta.objects.all()
    serializer_class = ParaderoRutaSerializer

class ParaderoRutaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParaderoRuta.objects.all()
    serializer_class = ParaderoRutaSerializer

class BusList(generics.ListCreateAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class BusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

class ViajeList(generics.ListCreateAPIView):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

class ViajeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer
