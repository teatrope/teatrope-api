import uuid
from django.db import models


class Teatro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True)
    calle = models.CharField(max_length=255)
    distrito = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self) -> str:
        return self.nombre


class Obra(models.Model):
    class Genero(models.TextChoices):
        DRAMA = 'DRAMA'
        COMEDIA = 'COMEDIA'
        MUSICAL = 'MUSICAL'
        EXPERIMENTAL = 'EXPERIMENTAL'

    class RolDir(models.TextChoices):
        ACTOR = 'ACTOR'
        DIRECTOR = 'DIRECTOR'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    teatro = models.ForeignKey(Teatro, on_delete=models.CASCADE, related_name='obras')
    titulo = models.CharField(max_length=255)
    genero = models.CharField(max_length=20, choices=Genero.choices)
    director_nombre = models.CharField(max_length=255)
    director_rol = models.CharField(max_length=20, choices=RolDir.choices, default=RolDir.DIRECTOR)

    def __str__(self) -> str:
        return self.titulo


class Funcion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='funciones')
    fecha = models.DateTimeField()
    duracion_minutos = models.IntegerField()
    disponibilidad_asientos = models.IntegerField()


class Persona(models.Model):
    class Rol(models.TextChoices):
        ACTOR = 'ACTOR'
        DIRECTOR = 'DIRECTOR'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='personas')
    nombre_completo = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=Rol.choices)

