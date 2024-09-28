from django.urls import path
from .views import (
    UsuarioList, UsuarioDetail,
    TarjetaList, TarjetaDetail,
    ParaderoList, ParaderoDetail,
    RecargaList, RecargaDetail,
    RutaList, RutaDetail,
    ParaderoRutaList, ParaderoRutaDetail,
    BusList, BusDetail,
    ViajeList, ViajeDetail,
)

urlpatterns = [
    path('usuarios/', UsuarioList.as_view(), name='usuario-list'),
    path('usuarios/<uuid:pk>/', UsuarioDetail.as_view(), name='usuario-detail'),
    
    path('tarjetas/', TarjetaList.as_view(), name='tarjeta-list'),
    path('tarjetas/<str:pk>/', TarjetaDetail.as_view(), name='tarjeta-detail'),
    
    path('paraderos/', ParaderoList.as_view(), name='paradero-list'),
    path('paraderos/<str:pk>/', ParaderoDetail.as_view(), name='paradero-detail'),
    
    path('recargas/', RecargaList.as_view(), name='recarga-list'),
    path('recargas/<uuid:pk>/', RecargaDetail.as_view(), name='recarga-detail'),
    
    path('rutas/', RutaList.as_view(), name='ruta-list'),
    path('rutas/<str:pk>/', RutaDetail.as_view(), name='ruta-detail'),
    
    path('paradero-rutas/', ParaderoRutaList.as_view(), name='paradero-ruta-list'),
    path('paradero-rutas/<int:pk>/', ParaderoRutaDetail.as_view(), name='paradero-ruta-detail'),
    
    path('buses/', BusList.as_view(), name='bus-list'),
    path('buses/<str:pk>/', BusDetail.as_view(), name='bus-detail'),
    
    path('viajes/', ViajeList.as_view(), name='viaje-list'),
    path('viajes/<uuid:pk>/', ViajeDetail.as_view(), name='viaje-detail'),
]
