from rest_framework import viewsets
from rest_framework import filters
from .models import Notificacion, RecomendacionPersonalizada, PreferenciasUsuario
from .serializers import NotificacionSerializer, RecomendacionPersonalizadaSerializer, PreferenciasUsuarioSerializer


class NotificacionViewSet(viewsets.ModelViewSet):
    queryset = Notificacion.objects.all()
    serializer_class = NotificacionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['tipo', 'contenido', 'titulo_mensaje', 'cuerpo_mensaje']


class RecomendacionPersonalizadaViewSet(viewsets.ModelViewSet):
    queryset = RecomendacionPersonalizada.objects.select_related('notificacion').all()
    serializer_class = RecomendacionPersonalizadaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['razon', 'notificacion__titulo_mensaje']


class PreferenciasUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PreferenciasUsuario.objects.all()
    serializer_class = PreferenciasUsuarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['frecuencia_notif', 'calle_preferida', 'distrito_preferida']

