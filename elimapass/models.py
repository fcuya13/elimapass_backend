import uuid
from django.db import models
from django.utils import timezone
import pytz
from django.core.exceptions import ValidationError

class Usuario(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    dni = models.CharField(max_length=50, unique=True, null=False)
    nombres = models.CharField(max_length=100, null=False)
    apellidos = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    recovery_token = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

class Tarjeta(models.Model):
    codigo = models.CharField(max_length=50, primary_key=True)
    saldo = models.FloatField(null=False)
    tipo = models.IntegerField(null=False)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    limite = models.FloatField(null=True)

    fecha_vencimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.codigo
    
class Paradero(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=False)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=False)

    def __str__(self):
        return self.nombre
    
class Recarga(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    fecha_hora = models.DateTimeField(default=lambda: timezone.now().astimezone(pytz.timezone('America/Lima')))
    codigo_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
    monto_recargado = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    medio_pago = models.CharField(max_length=50, null=False)

    def __str__(self):
        return f'{self.codigo_tarjeta} - {self.monto_recargado}'

class Ruta(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100, null=False)
    servicio = models.CharField(max_length=100, null=False)
    inicio = models.CharField(max_length=100, null=False)
    final = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.nombre


class ParaderoRuta(models.Model):
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    id_paradero = models.ForeignKey(Paradero, on_delete=models.CASCADE)
    sentido_ida = models.BooleanField(default=True)

    class Meta:
        unique_together = (('id_ruta', 'id_paradero'),)

    def __str__(self):
        return f'{self.id_paradero.id} - {self.id_ruta.nombre}'

class Bus(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.id

class Tarifa(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    id_ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    precio_base = models.FloatField(null=False)


class Viaje(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    fecha_hora = models.DateTimeField(null=False)
    id_tarifa = models.ForeignKey(Tarifa, on_delete=models.CASCADE)
    codigo_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE)
    precio_final = models.FloatField(null=False)

    bus_id = models.ForeignKey(Bus, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.id_tarifa.id_ruta.nombre} - {self.id_tarifa.precio_base}'

class Solicitud(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    dni_frontal = models.ImageField(upload_to='solicitudes/dni/', null=False, blank=False)
    dni_reversa = models.ImageField(upload_to='solicitudes/dni/', null=False, blank=False)
    carnet_frontal = models.ImageField(upload_to='solicitudes/carnet/', null=False, blank=False)
    carnet_reversa = models.ImageField(upload_to='solicitudes/carnet/', null=False, blank=False)

    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    codigo_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=True, blank=True)


    def clean(self):
        if not self.id_usuario and not self.codigo_tarjeta:
            raise ValidationError('Debe asociarse a un usuario o a una tarjeta.')
        if self.id_usuario and self.codigo_tarjeta:
            raise ValidationError('No puede asociarse simultáneamente a un usuario y a una tarjeta.')

    def __str__(self):
        return f'Solicitud de {self.id_usuario or self.codigo_tarjeta}'


