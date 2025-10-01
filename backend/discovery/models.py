import uuid
from django.db import models


class Busqueda(models.Model):
    class Genero(models.TextChoices):
        DRAMA = 'DRAMA'
        COMEDIA = 'COMEDIA'
        MUSICAL = 'MUSICAL'
        EXPERIMENTAL = 'EXPERIMENTAL'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    usuario_id = models.UUIDField()
    timestamp = models.DateTimeField(auto_now_add=True)
    genero_filtro = models.CharField(max_length=20, choices=Genero.choices, blank=True)
    calle_filtro = models.CharField(max_length=255, blank=True)
    distrito_filtro = models.CharField(max_length=100, blank=True)
    latitud_filtro = models.FloatField(null=True, blank=True)
    longitud_filtro = models.FloatField(null=True, blank=True)
    fecha_inicio = models.DateTimeField(null=True, blank=True)
    fecha_fin = models.DateTimeField(null=True, blank=True)


class ObraVistaCache(models.Model):
    class Genero(models.TextChoices):
        DRAMA = 'DRAMA'
        COMEDIA = 'COMEDIA'
        MUSICAL = 'MUSICAL'
        EXPERIMENTAL = 'EXPERIMENTAL'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titulo = models.CharField(max_length=255)
    genero = models.CharField(max_length=20, choices=Genero.choices)
    calle = models.CharField(max_length=255)
    distrito = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()
    funciones_json = models.JSONField(default=list)


class Recomendacion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    busqueda = models.ForeignKey(Busqueda, on_delete=models.CASCADE, related_name='recomendaciones')
    obra = models.ForeignKey(ObraVistaCache, on_delete=models.CASCADE, related_name='recomendaciones')
    puntuacion = models.FloatField()
    razon = models.TextField(blank=True)

