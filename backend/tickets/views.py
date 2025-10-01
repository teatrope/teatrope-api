from rest_framework import viewsets
from .models import Reserva, DetalleEntrada, DisponibilidadCache
from .serializers import ReservaSerializer, DetalleEntradaSerializer, DisponibilidadCacheSerializer


class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class DetalleEntradaViewSet(viewsets.ModelViewSet):
    queryset = DetalleEntrada.objects.select_related('reserva').all()
    serializer_class = DetalleEntradaSerializer


class DisponibilidadCacheViewSet(viewsets.ModelViewSet):
    queryset = DisponibilidadCache.objects.all()
    serializer_class = DisponibilidadCacheSerializer

