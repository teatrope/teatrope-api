import uuid
from django.db import models


class Reserva(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'PENDIENTE'
        CONFIRMADA = 'CONFIRMADA'
        CANCELADA = 'CANCELADA'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario_id = models.UUIDField()
    funcion_id = models.UUIDField()
    cantidad = models.IntegerField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.PENDIENTE)
    timestamp = models.DateTimeField(auto_now_add=True)
    codigo_qr = models.CharField(max_length=255, blank=True)
    detalles_ticket = models.TextField(blank=True)


class DetalleEntrada(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, related_name='detalles')
    asiento = models.CharField(max_length=50)
    precio = models.FloatField()


class DisponibilidadCache(models.Model):
    funcion_id = models.UUIDField(primary_key=True)
    total_asientos = models.IntegerField()
    disponibles = models.IntegerField()
    ultima_actualizacion = models.DateTimeField(auto_now=True)

