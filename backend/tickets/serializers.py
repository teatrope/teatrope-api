from rest_framework import serializers
from .models import Reserva, DetalleEntrada, DisponibilidadCache


class DetalleEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleEntrada
        fields = '__all__'


class ReservaSerializer(serializers.ModelSerializer):
    detalles = DetalleEntradaSerializer(many=True, read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'


class DisponibilidadCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadCache
        fields = '__all__'

