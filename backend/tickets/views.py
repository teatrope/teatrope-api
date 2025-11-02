from rest_framework import viewsets
from rest_framework import filters
from .models import Reserva, DetalleEntrada, DisponibilidadCache
from .serializers import ReservaSerializer, DetalleEntradaSerializer, DisponibilidadCacheSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['estado', 'codigo_qr', 'detalles_ticket']


class DetalleEntradaViewSet(viewsets.ModelViewSet):
    queryset = DetalleEntrada.objects.select_related('reserva').all()
    serializer_class = DetalleEntradaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['asiento', 'reserva__estado']


class DisponibilidadCacheViewSet(viewsets.ModelViewSet):
    queryset = DisponibilidadCache.objects.all()
    serializer_class = DisponibilidadCacheSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = []

