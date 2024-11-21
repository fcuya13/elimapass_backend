from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('tarjetas/<str:codigo_tarjeta>/saldo/', SaldoTarjetaView.as_view(), name='saldo-tarjeta'),
    path('tarjetas/<str:codigo_tarjeta>/viajes/', ListaViajesPorTarjetaView.as_view(), name='lista-viajes-tarjeta'),
    path('tarjetas/<str:codigo_tarjeta>/cambiar-limite/', CambiarLimiteTarjetaView.as_view(), name='cambiar-limite-tarjeta'),

    path('recovery/', RecuperarPassword.as_view(), name='recuperar-password'),
    path('recovery/<str:recovery_token>/', UpdatePasswordView.as_view(), name='update-password'),

    path('pagar_viaje/', PagarTarifa.as_view(), name='pago'),

    path('tarjetas/<str:codigo_tarjeta>/recargas/', HistorialRecargasView.as_view(), name='historial_recargas'),

    path('buses/', BusList.as_view(), name='bus-list'),

    path('recargar/', RecargarTarjetaView.as_view(), name='recargar_tarjeta'),

    path('paraderos/<str:codigo_ruta>/', ParaderosRuta.as_view(), name='paraderos'),


    path('rutas/', RutaList.as_view(), name='ruta_list'),
    ]
