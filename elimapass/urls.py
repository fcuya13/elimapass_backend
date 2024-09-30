from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    
    path('usuarios/', UsuarioList.as_view(), name='usuario-list'),
    path('usuarios/<uuid:pk>/', UsuarioDetail.as_view(), name='usuario-detail'),
    
    path('tarjetas/', TarjetaList.as_view(), name='tarjeta-list'),
    path('tarjetas/<str:pk>/', TarjetaDetail.as_view(), name='tarjeta-detail'),

    path('recargas/', RecargaList.as_view(), name='recarga-list'),
    path('recargas/<uuid:pk>/', RecargaDetail.as_view(), name='recarga-detail'),
    
    path('viajes/', ViajeList.as_view(), name='viaje-list'),
    path('viajes/<uuid:pk>/', ViajeDetail.as_view(), name='viaje-detail'),
]
