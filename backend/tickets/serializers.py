from rest_framework import serializers
from .models import Reserva, DetalleEntrada, DisponibilidadCache


class DetalleEntradaSerializer(serializers.ModelSerializer):
    reserva = serializers.PrimaryKeyRelatedField(queryset=Reserva.objects.all(), help_text='ID of the associated reservation (UUID)')

    class Meta:
        model = DetalleEntrada
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique ticket detail ID (UUID)'},
            'asiento': {'help_text': 'Seat identifier'},
            'precio': {'help_text': 'Price'},
        }

    def validate_reserva(self, value):
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Nest the related reservation object for read operations
        representation['reserva'] = ReservaSerializer(instance.reserva).data
        return representation


class ReservaSerializer(serializers.ModelSerializer):
    detalles = DetalleEntradaSerializer(many=True, read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique reservation ID (UUID)'},
            'usuario_id': {'help_text': 'User ID (UUID)'},
            'funcion_id': {'help_text': 'Function ID (UUID)'},
            'cantidad': {'help_text': 'Quantity'},
            'estado': {'help_text': 'Reservation status (e.g., PENDIENTE)'},
            'timestamp': {'help_text': 'Reservation timestamp'},
            'codigo_qr': {'help_text': 'QR code'},
            'detalles_ticket': {'help_text': 'Ticket details text'},
            'detalles': {'help_text': 'List of ticket details'},
        }


class DisponibilidadCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisponibilidadCache
        fields = '__all__'
        extra_kwargs = {
            'funcion_id': {'help_text': 'Function ID (UUID)'},
            'total_asientos': {'help_text': 'Total seats'},
            'disponibles': {'help_text': 'Available seats'},
            'ultima_actualizacion': {'help_text': 'Last update timestamp'},
        }

