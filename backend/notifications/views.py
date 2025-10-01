from rest_framework import viewsets
from .models import Notificacion, RecomendacionPersonalizada, PreferenciasUsuario
from .serializers import NotificacionSerializer, RecomendacionPersonalizadaSerializer, PreferenciasUsuarioSerializer


class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer


class RecomendacionPersonalizadaViewSet(viewsets.ModelViewSet):
    queryset = RecomendacionPersonalizada.objects.select_related('notificacion').all()
    serializer_class = RecomendacionPersonalizadaSerializer


class PreferenciasUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PreferenciasUsuario.objects.all()
    serializer_class = PreferenciasUsuarioSerializer

