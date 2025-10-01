from rest_framework import viewsets
from .models import Busqueda, Recomendacion, ObraVistaCache
from .serializers import BusquedaSerializer, RecomendacionSerializer, ObraVistaCacheSerializer


class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busqueda.objects.all()
    serializer_class = BusquedaSerializer


class RecomendacionViewSet(viewsets.ModelViewSet):
    queryset = Recomendacion.objects.select_related('busqueda', 'obra').all()
    serializer_class = RecomendacionSerializer


class ObraVistaCacheViewSet(viewsets.ModelViewSet):
    queryset = ObraVistaCache.objects.all()
    serializer_class = ObraVistaCacheSerializer

