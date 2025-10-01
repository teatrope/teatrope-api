import uuid
from django.db import models


class Notificacion(models.Model):
    class Tipo(models.TextChoices):
        ESTRENO = 'ESTRENO'
        CAMBIO_FUNCION = 'CAMBIO_FUNCION'
        RECOMENDACION = 'RECOMENDACION'

    class Estado(models.TextChoices):
        ENVIADA = 'ENVIADA'
        LEIDA = 'LEIDA'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario_id = models.UUIDField()
    tipo = models.CharField(max_length=30, choices=Tipo.choices)
    contenido = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ENVIADA)
    titulo_mensaje = models.CharField(max_length=100)
    cuerpo_mensaje = models.TextField()
    enlace_mensaje = models.CharField(max_length=255, blank=True)


class RecomendacionPersonalizada(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE, related_name='recomendaciones')
    obra_id = models.UUIDField()
    score_relevancia = models.FloatField()
    razon = models.TextField(blank=True)


class PreferenciasUsuario(models.Model):
    usuario_id = models.UUIDField(primary_key=True)
    generos_json = models.JSONField(default=list)
    calle_preferida = models.CharField(max_length=255, blank=True)
    distrito_preferida = models.CharField(max_length=100, blank=True)
    latitud_preferida = models.FloatField(null=True, blank=True)
    longitud_preferida = models.FloatField(null=True, blank=True)
    frecuencia_notif = models.CharField(max_length=20, choices=[('DIARIA', 'DIARIA'), ('SEMANAL', 'SEMANAL')], default='SEMANAL')

