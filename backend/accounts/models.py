import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class Usuario(AbstractUser):
    class Rol(models.TextChoices):
        CONSUMIDOR = 'CONSUMIDOR'
        TEATRO = 'TEATRO'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    tipo_rol = models.CharField(max_length=20, choices=Rol.choices, default=Rol.CONSUMIDOR)
    permisos_json = models.JSONField(default=list, blank=True)
    generos_preferidos_json = models.JSONField(default=list, blank=True)
    calle_preferida = models.CharField(max_length=255, blank=True)
    distrito_preferida = models.CharField(max_length=100, blank=True)
    latitud_preferida = models.FloatField(null=True, blank=True)
    longitud_preferida = models.FloatField(null=True, blank=True)
    ultimo_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    def __str__(self) -> str:
        return self.email

