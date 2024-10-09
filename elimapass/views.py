from rest_framework import generics
from .models import *
from .serializer import *
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializer import SignUpSerializer, LoginSerializer
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.crypto import get_random_string

class Test(APIView):
    def get (self, request):
        try:
            """
            2. mandar link /recovery/token por correo si es que está validado dni+correo
            3. crear view que funcione desde internet (?) - picante
            4. reemplazar pwd y borrar token, si el token no existe que te putee
            """
            ##GENERAR RECOVER TOKEN
            baseurl = request.build_absolute_uri()

            recovery_token = get_random_string(length=42)
            usuario.recovery_token = recovery_token
            usuario.save()
             
            ##correo
            email = EmailMessage(
                'Recuperación de Contraseña',
                f'Sigue este enlace para recuperar tu contraseña: {baseurl}{recovery_token}/',
                settings.EMAIL_HOST_USER,
                [usuario.email],
                fail_silently=False,
            )
            email.send()
        
            return Response(status=status.HTTP_200_OK)
        
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



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

class TarjetaList(generics.ListCreateAPIView):
    queryset = Tarjeta.objects.all()
    serializer_class = TarjetaSerializer

class TarjetaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tarjeta.objects.all()
    serializer_class = TarjetaSerializer

class RecargaList(generics.ListCreateAPIView):
    queryset = Recarga.objects.all()
    serializer_class = RecargaSerializer

class RecargaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recarga.objects.all()
    serializer_class = RecargaSerializer

class ViajeList(generics.ListCreateAPIView):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer

class ViajeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Viaje.objects.all()
    serializer_class = ViajeSerializer
