from rest_framework import serializers
from .models import Reserva, DetalleEntrada, DisponibilidadCache


class DetalleEntradaSerializer(serializers.ModelSerializer):
    reserva = serializers.PrimaryKeyRelatedField(read_only=True, help_text='Associated reservation')

    class Meta:
        model = DetalleEntrada
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique ticket detail ID'},
            'reserva': {'help_text': 'Associated reservation'},
            'asiento': {'help_text': 'Seat number'},
            'precio': {'help_text': 'Ticket price'},
        }


class ReservaSerializer(serializers.ModelSerializer):
    detalles = DetalleEntradaSerializer(many=True, read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique reservation ID'},
            'usuario_id': {'help_text': 'User ID'},
            'funcion_id': {'help_text': 'Function ID'},
            'cantidad': {'help_text': 'Number of tickets'},
            'estado': {'help_text': 'Reservation state'},
            'timestamp': {'help_text': 'Reservation timestamp'},
            'codigo_qr': {'help_text': 'QR code for the reservation'},
            'detalles_ticket': {'help_text': 'Ticket details'},
        }


class DisponibilidadCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadCache
        fields = '__all__'
        extra_kwargs = {
            'funcion_id': {'help_text': 'Function ID'},
            'total_asientos': {'help_text': 'Total seats'},
            'disponibles': {'help_text': 'Available seats'},
            'ultima_actualizacion': {'help_text': 'Last update time'},
        }

