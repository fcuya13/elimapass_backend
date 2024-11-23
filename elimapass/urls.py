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

    path('solicitudes/', SolicitudAPIView.as_view(), name='solicitud-list-create'),

    path('solicitudes/<str:solicitud_id>/', SolicitudDetailAPIView.as_view(), name='solicitud-detail-accept'),

    path('dashboard/viajes-por-linea/', viajes_por_linea, name='viajes-por-linea'),
    path('dashboard/promedio-recarga-por-usuario/', promedio_recarga_por_usuario, name='promedio-recarga-por-usuario'),
    path('dashboard/promedio-viajes-por-usuario/', promedio_viajes_por_usuario, name='promedio-viajes-por-usuario'),
    path('dashboard/total-usuarios-registrados/', total_usuarios_registrados, name='total-usuarios-registrados'),
    path('dashboard/recargas-por-hora/', recargas_por_hora, name='recargas-por-hora'),
    path('dashboard/medio-pago-mas-usado/', medio_pago_mas_usado, name='medio-pago-mas-usado'),
    path('dashboard/viajes-por-hora/', viajes_por_hora, name='viajes_por_hora'),

    path('admin/register/', AdminUserRegisterView.as_view(), name='admin-register'),
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    ]
