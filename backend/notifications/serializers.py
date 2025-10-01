from rest_framework import serializers
from .models import Notificacion, RecomendacionPersonalizada, PreferenciasUsuario


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'


class RecomendacionPersonalizadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecomendacionPersonalizada
        fields = '__all__'


class PreferenciasUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenciasUsuario
        fields = '__all__'

