import os
import uuid
from django.db import models, transaction, IntegrityError
from django.db.models import UniqueConstraint, Q
from django.utils import timezone

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
    fecha_hora = models.DateTimeField(default=timezone.now())
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

class AdminUsuario(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    dni = models.CharField(max_length=50, unique=True, null=False)
    nombres = models.CharField(max_length=100, null=False)
    apellidos = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=100, null=False)
    rol = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('superadmin', 'Superadmin')], default='admin')

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

class Solicitud(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    dni_frontal = models.ImageField(upload_to='solicitudes/dni/', null=False, blank=False)
    dni_reversa = models.ImageField(upload_to='solicitudes/dni/', null=False, blank=False)
    carnet_frontal = models.ImageField(upload_to='solicitudes/carnet/', null=False, blank=False)
    carnet_reversa = models.ImageField(upload_to='solicitudes/carnet/', null=False, blank=False)

    codigo_tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=False, blank=True)

    estado = models.CharField(max_length=20, choices=[('pendiente', 'Pendiente'), ('aceptada', 'Aceptada'), ('rechazada', 'Rechazada')],
        default='pendiente')
    admin_user = models.ForeignKey(AdminUsuario, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['codigo_tarjeta'],
                condition=Q(estado='pendiente'),
                name='unique_codigo_tarjeta_pendiente'
            )
        ]

    def delete(self, *args, **kwargs):
        # Eliminar los archivos asociados antes de eliminar la instancia.
        self._delete_uploaded_files()
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Usar una transacción para asegurar consistencia.
        try:
            with transaction.atomic():
                super().save(*args, **kwargs)
        except IntegrityError as e:
            self._delete_uploaded_files()
            raise e

    def _delete_uploaded_files(self):
        """
        Elimina los archivos subidos si no se guarda la instancia.
        """
        fields = ['dni_frontal', 'dni_reversa', 'carnet_frontal', 'carnet_reversa']
        for field in fields:
            file = getattr(self, field)
            if file and os.path.isfile(file.path):  # Verifica que el archivo existe.
                os.remove(file.path)

    def __str__(self):
        return f'Solicitud de {self.codigo_tarjeta}'
