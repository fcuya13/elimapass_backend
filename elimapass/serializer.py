from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from random import randint

class RecuperarContrasenaSerializer(serializers.Serializer):
    dni = serializers.CharField(max_length=50)
    email = serializers.EmailField()

    def validate(self, attrs):
        try:
            Usuario.objects.get(dni=attrs['dni'], email=attrs['email'])
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("No existe un usuario con este DNI y correo.")
        return attrs

class SignUpSerializer(serializers.ModelSerializer):

    num_tarjeta  = serializers.CharField(write_only=True, allow_null=True, required=False)

    class Meta:
        model = Usuario
        fields = ('dni', 'nombres', 'apellidos', 'email', 'password', 'num_tarjeta')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        numero_tarjeta = validated_data.pop('num_tarjeta', None)
        validated_data['password'] = make_password(validated_data['password'])
        user = Usuario(**validated_data)
        user.save()
        if not numero_tarjeta:
            Tarjeta.objects.create(
                codigo=str(randint(1000000000, 9999999999)),
                id_usuario=user,
                saldo=0,
                tipo=0,
                limite=0
            )
            return user
        if len(numero_tarjeta) != 10:
            raise serializers.ValidationError('Numero de tarjeta invalida')
        Tarjeta.objects.create(
            codigo=numero_tarjeta,
            id_usuario=user,
            saldo=10,
            tipo=0,
            limite=0
        )
        return user

class LoginSerializer(serializers.Serializer):
    dni = serializers.CharField()
    password = serializers.CharField()


class ParaderoRutaSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='id_paradero.id')
    nombre = serializers.CharField(source='id_paradero.nombre')
    latitud = serializers.DecimalField(source='id_paradero.latitud', max_digits=9, decimal_places=6)
    longitud = serializers.DecimalField(source='id_paradero.longitud', max_digits=9, decimal_places=6)
    sentido_ida = serializers.BooleanField()

    class Meta:
        model = ParaderoRuta
        fields = ['id', 'nombre', 'latitud', 'longitud', 'sentido_ida']

