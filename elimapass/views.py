from collections import defaultdict
from django.db.models.functions import ExtractHour
from django.http import JsonResponse
from rest_framework.decorators import api_view

from .serializer import *
from django.contrib.auth.hashers import make_password, check_password
from .models import *
from .serializer import SignUpSerializer, LoginSerializer, SolicitudSerializer
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404, render
from .forms import PasswordUpdateForm
from .models import Tarifa, Viaje
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Tarjeta, Recarga
from .serializer import RecargaSerializer
from django.db.models import Count, Avg, Sum
from django.db.models.functions import TruncHour

class UpdatePasswordView(APIView):
    def get(self, request, recovery_token):
        get_object_or_404(Usuario, recovery_token=recovery_token)
        form = PasswordUpdateForm()
        return render(request, 'update_password.html', {'form': form})

    def post(self, request, recovery_token):
        usuario_to_update = get_object_or_404(Usuario, recovery_token=recovery_token)

        form = PasswordUpdateForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            usuario_to_update.password = make_password(new_password)
            usuario_to_update.recovery_token = None
            usuario_to_update.save()
            return Response({"message": "Contraseña actualizada con éxito."}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


class ParaderosRuta(APIView):
    def get(self, request, codigo_ruta):
        try:
            paraderos_ruta = ParaderoRuta.objects.filter(id_ruta__id=codigo_ruta).select_related('id_paradero', 'id_ruta')

            serializer = ParaderoRutaSerializer(paraderos_ruta, many=True)

            return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False,
                                json_dumps_params=dict(ensure_ascii=False))
        except Ruta.DoesNotExist:
            return JsonResponse({'error': 'Ruta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
class RecuperarPassword(APIView):
    def post (self, request):

        serializer = RecuperarContrasenaSerializer(data=request.data)

        if serializer.is_valid():
            usuario = Usuario.objects.get(dni=serializer.validated_data['dni'], email=serializer.validated_data['email'])
            recovery_token = get_random_string(length=32)
            usuario.recovery_token = recovery_token
            usuario.save()
        try:
            baseurl = settings.BASE_URL
            print(baseurl)
            email = EmailMessage(
                'Recuperación de Contraseña',
                f'Sigue este enlace para recuperar tu contraseña: {baseurl}elimapass/v1/recovery/{recovery_token}/',
                settings.EMAIL_HOST_USER,
                [usuario.email],
            )
            email.send()

            return Response({recovery_token}, status=status.HTTP_200_OK)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class HistorialRecargasView(APIView):
    def get(self, request, codigo_tarjeta):
        try:
            tarjeta = Tarjeta.objects.get(codigo=codigo_tarjeta)
            recargas = Recarga.objects.filter(codigo_tarjeta=tarjeta).order_by("-fecha_hora")[:10]
            
            lista_recargas = [
                {
                    "id": str(recarga.id),
                    "fecha": recarga.fecha_hora.isoformat(),
                    "monto_recargado": recarga.monto_recargado,
                    "medio_pago": recarga.medio_pago,
                }
                for recarga in recargas
            ]
            
            return Response({
                "codigo_tarjeta": tarjeta.codigo,
                "recargas": lista_recargas
            }, status=status.HTTP_200_OK)
        except Tarjeta.DoesNotExist:
            return Response({"error": "Tarjeta no existe"}, status=status.HTTP_404_NOT_FOUND)

class SaldoTarjetaView(APIView):
    def get(self, request, codigo_tarjeta):
        try:
            tarjeta = Tarjeta.objects.get(codigo=codigo_tarjeta)
            return Response({
                "codigo_tarjeta": tarjeta.codigo,
                "saldo": tarjeta.saldo
            }, status=status.HTTP_200_OK)
        except Tarjeta.DoesNotExist:
            return Response({"error": "Tarjeta no existe"}, status=status.HTTP_404_NOT_FOUND)
        
class SignUpView(APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"id": user.id, "nombres": user.nombres}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PagarTarifa(APIView):
    def post(self, request):
        codigo_tarjeta = request.data.get('tarjetaId')
        id_bus = request.data.get('busId')

        if not codigo_tarjeta or not id_bus:
            return Response({"error": "Debe proporcionar codigo_tarjeta e id_tarifa."}, status=status.HTTP_400_BAD_REQUEST)

        tarjeta = get_object_or_404(Tarjeta, codigo=codigo_tarjeta)
        bus = Bus.objects.get(id=id_bus)
        tarifa = Tarifa.objects.get(id_ruta=bus.id_ruta)

        precio_final = tarifa.precio_base

        if tarjeta.tipo == 1:
            precio_final = round(tarifa.precio_base / 2, 2)

        if tarjeta.saldo < precio_final:
            return Response({"error": "Saldo insuficiente."}, status=status.HTTP_400_BAD_REQUEST)

        tarjeta.saldo -= precio_final
        tarjeta.save()

        Viaje.objects.create(
            fecha_hora=datetime.now(),
            id_tarifa=tarifa,
            codigo_tarjeta=tarjeta,
            precio_final=precio_final,
            bus_id=bus
        )
        return Response({
            "mensaje": "Pago realizado con éxito.",
            "saldo_actual": round(tarjeta.saldo, 2),
        }, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            dni = serializer.validated_data['dni']
            password = serializer.validated_data['password']
            try:
                user = Usuario.objects.get(dni=dni)
                tarjeta = Tarjeta.objects.get(id_usuario=user)
                if check_password(password, user.password):
                    return Response({
                        "id": user.id,
                        "tarjeta": tarjeta.codigo,
                        "tipo": tarjeta.tipo
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({"error": "Usuario no existe"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CambiarLimiteTarjetaView(APIView):
    def put(self, request, codigo_tarjeta):
        try:
            tarjeta = Tarjeta.objects.get(codigo=codigo_tarjeta)
            nuevo_limite = request.data.get('limite')

            if nuevo_limite is not None:
                tarjeta.limite = nuevo_limite
                tarjeta.save()
                return Response({
                    "codigo_tarjeta": tarjeta.codigo,
                    "nuevo_limite": tarjeta.limite
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Límite no proporcionado"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Tarjeta.DoesNotExist:
            return Response({"error": "Tarjeta no existe"}, status=status.HTTP_404_NOT_FOUND)
        
class ListaViajesPorTarjetaView(APIView):
    def get(self, request, codigo_tarjeta):
        try:
            tarjeta = Tarjeta.objects.get(codigo=codigo_tarjeta)
            viajes = Viaje.objects.filter(codigo_tarjeta=tarjeta).order_by("-fecha_hora")[:10]
            
            lista_viajes = [
                {
                    "id": viaje.id,
                    "fecha_hora": viaje.fecha_hora,
                    "ruta": viaje.id_tarifa.id_ruta.nombre,
                    "precio_final": viaje.precio_final
                }
                for viaje in viajes
            ]
            
            return Response({
                "codigo_tarjeta": tarjeta.codigo,
                "viajes": lista_viajes
            }, status=status.HTTP_200_OK)
        except Tarjeta.DoesNotExist:
            return Response({"error": "Tarjeta no existe"}, status=status.HTTP_404_NOT_FOUND)

class RutaList(APIView):
    def get(self, request):
        queryset = Ruta.objects.all().order_by("nombre")

        rutas_por_servicio = defaultdict(list)

        for ruta in queryset:
            rutas_por_servicio[ruta.servicio].append({
                "id": ruta.id,
                "nombre": ruta.nombre,
                "inicio": ruta.inicio,
                "final": ruta.final
            })

        rutas_agrupadas = dict(rutas_por_servicio)

        return Response(rutas_agrupadas, status=status.HTTP_200_OK)

class BusList(APIView):
    def get(self, request):
        queryset = Bus.objects.all()

        lista_buses = [
            {
                "id": bus.id,
                "nombre": bus.id_ruta.nombre
            }
        for bus in queryset
        ]

        return Response(lista_buses)
    
class RecargarTarjetaView(APIView):
    def post(self, request):
        serializer = RecargaSerializer(data=request.data)
        if serializer.is_valid():
            codigo_tarjeta = serializer.validated_data['codigo_tarjeta']
            monto_recargado = serializer.validated_data['monto_recargado']
            medio_pago = serializer.validated_data['medio_pago']

            tarjeta = Tarjeta.objects.get(codigo=codigo_tarjeta)
            tarjeta.saldo += float(monto_recargado)
            tarjeta.save()

            recarga = Recarga.objects.create(
                codigo_tarjeta=tarjeta,
                monto_recargado=monto_recargado,
                medio_pago=medio_pago
            )

            return Response({
                "mensaje": "Recarga realizada con éxito",
                "tarjeta": tarjeta.codigo,
                "saldo_actualizado": tarjeta.saldo,
                "recarga_id": recarga.id
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SolicitudAPIView(APIView):
    def post(self, request):
        serializer = SolicitudSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        solicitudes = Solicitud.objects.all()
        serializer = SolicitudSerializer(solicitudes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SolicitudDetailAPIView(APIView):
    def get(self, request, solicitud_id):
        solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
        serializer = SolicitudSerializer(solicitud)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, solicitud_id):
        # Buscar la solicitud
        solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

        # Validar el estado recibido en el cuerpo de la solicitud
        estado = request.data.get('estado')
        if estado not in ['aceptada', 'rechazada']:
            return Response(
                {'error': 'El estado debe ser "aceptada" o "rechazada".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Actualizar el estado
        solicitud.estado = estado
        tarjeta = solicitud.codigo_tarjeta
        tarjeta.fecha_vencimiento = timezone.now() + timedelta(days=365)
        tarjeta.save()
        solicitud.save()

        return Response(
            {'message': f'Solicitud con ID {solicitud_id} actualizada exitosamente a estado "{estado}".'},
            status=status.HTTP_200_OK
        )

class AdminLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            dni = serializer.validated_data['dni']
            password = serializer.validated_data['password']
            try:
                user = AdminUsuario.objects.get(dni=dni)
                if check_password(password, user.password):
                    return Response({
                        "user": user.id,
                    }, status=status.HTTP_200_OK)
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except Usuario.DoesNotExist:
                return Response({"error": "Usuario no existe"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserRegisterView(APIView):
    def post(self, request):
        """
        Endpoint para registrar un nuevo usuario administrador.
        """
        serializer = AdminUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Encriptar la contraseña
            data['password'] = make_password(data['password'])

            # Crear el usuario administrador
            try:
                admin_user = AdminUsuario.objects.create(**data)
                return Response(
                    {"message": "Usuario administrador creado exitosamente", "user_id": admin_user.id},
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": "No se pudo crear el usuario administrador", "details": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def viajes_por_linea(request):
    fecha = request.GET.get('fecha', timezone.now().date())
    viajes = Viaje.objects.filter(fecha_hora__date=fecha).values('id_tarifa__id_ruta__nombre') \
        .annotate(cantidad=Count('id')) \
        .order_by('id_tarifa__id_ruta__nombre')
    return Response(viajes)

@api_view(['GET'])
def promedio_recarga_por_usuario(request):
    promedio = Recarga.objects.aggregate(promedio=Avg('monto_recargado'))
    promedio_redondeado = round(promedio['promedio'], 2) if promedio['promedio'] is not None else 0
    return Response({'cantidad': promedio_redondeado})

@api_view(['GET'])
def promedio_viajes_por_usuario(request):
    promedio = Viaje.objects.values('codigo_tarjeta__id_usuario').annotate(promedio=Avg('id')).count()
    return Response({'cantidad': promedio})

@api_view(['GET'])
def total_usuarios_registrados(request):
    usuarios = Usuario.objects.count()
    return Response({'cantidad': usuarios})

@api_view(['GET'])
def recargas_por_hora(request):
    fecha = request.GET.get('fecha', timezone.now().date())
    recargas = Recarga.objects.filter(fecha_hora__date=fecha).annotate(hora=TruncHour('fecha_hora')) \
        .values('hora') \
        .annotate(total=Sum('monto_recargado')) \
        .order_by('hora')
    return Response(recargas)

@api_view(['GET'])
def medio_pago_mas_usado(request):
    # Obtener datos agregados por medio de pago
    medios = Recarga.objects.values('medio_pago').annotate(cantidad=Count('id')).order_by('-cantidad')

    # Formatear los datos para que coincidan con el formato esperado
    data = [{"tipo": medio["medio_pago"], "cantidad": medio["cantidad"]} for medio in medios]

    return Response(data)

@api_view(['GET'])
def viajes_por_hora(request):
    """
    Retorna la cantidad de viajes por hora para un día y una ruta específica.
    """
    # Obtener parámetros de la solicitud
    fecha = request.query_params.get('fecha')  # Debe estar en formato 'YYYY-MM-DD'
    ruta_nombre = request.query_params.get('ruta_nombre')  # Nombre de la ruta

    # Validar los parámetros
    if not fecha or not ruta_nombre:
        return Response(
            {'error': 'Los parámetros "fecha" y "ruta_nombre" son obligatorios.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')  # Convertir a objeto datetime
    except ValueError:
        return Response(
            {'error': 'El parámetro "fecha" debe estar en formato "YYYY-MM-DD".'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validar que la ruta exista
    try:
        ruta = Ruta.objects.get(nombre=ruta_nombre)
    except Ruta.DoesNotExist:
        return Response({'error': f'La ruta con nombre "{ruta_nombre}" no existe.'}, status=status.HTTP_404_NOT_FOUND)

    # Filtrar viajes por fecha y ruta
    viajes = (
        Viaje.objects.filter(fecha_hora__date=fecha_obj, id_tarifa__id_ruta=ruta)
        .annotate(hora=ExtractHour('fecha_hora'))  # Extraer la hora del campo fecha_hora
        .values('hora')  # Agrupar por hora
        .annotate(cantidad_viajes=Count('id'))  # Contar los viajes por hora
        .order_by('hora')  # Ordenar por la hora
    )

    # Crear un diccionario de horas con valores de cantidad de viajes
    viajes_dict = {viaje['hora']: viaje['cantidad_viajes'] for viaje in viajes}

    # Generar un resultado con todas las horas de 0 a 23
    resultados = [
        {
            'hora': hora,
            'cantidad_viajes': viajes_dict.get(hora, 0)  # Usar el valor de viajes o 0 si no está presente
        }
        for hora in range(24)  # Rango de 0 a 23
    ]

    # Responder con los resultados
    return Response({
        'ruta': ruta.nombre,
        'fecha': fecha,
        'resultados': resultados
    }, status=status.HTTP_200_OK)
