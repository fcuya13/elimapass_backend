from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('tarjetas/', TarjetaList.as_view(), name='tarjeta-list'),
    path('tarjetas/<str:pk>/', TarjetaDetail.as_view(), name='tarjeta-detail'),
    path('tarjetas/<str:codigo_tarjeta>/saldo/', SaldoTarjetaView.as_view(), name='saldo-tarjeta'),
    path('tarjetas/<str:codigo_tarjeta>/viajes/', ListaViajesPorTarjetaView.as_view(), name='lista-viajes-tarjeta'),
    path('tarjetas/<str:codigo_tarjeta>/cambiar-limite/', CambiarLimiteTarjetaView.as_view(), name='cambiar-limite-tarjeta'),

    path('recargas/', RecargaList.as_view(), name='recarga-list'),
    path('recargas/<uuid:pk>/', RecargaDetail.as_view(), name='recarga-detail'),
    
    path('viajes/', ViajeList.as_view(), name='viaje-list'),
    path('viajes/<uuid:pk>/', ViajeDetail.as_view(), name='viaje-detail'),

    path('recovery/', RecuperarPassword.as_view(), name='recuperar-password'),
    path('recovery/<str:recovery_token>/', UpdatePasswordView.as_view(), name='update-password')
]
