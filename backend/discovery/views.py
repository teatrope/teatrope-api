from rest_framework import viewsets
from rest_framework import filters
from .models import Busqueda, Recomendacion, ObraVistaCache
from .serializers import BusquedaSerializer, RecomendacionSerializer, ObraVistaCacheSerializer


class BusquedaViewSet(viewsets.ModelViewSet):
    queryset = Busqueda.objects.all()
    serializer_class = BusquedaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['genero_filtro', 'calle_filtro', 'distrito_filtro']


class RecomendacionViewSet(viewsets.ModelViewSet):
    queryset = Recomendacion.objects.select_related('busqueda', 'obra').all()
    serializer_class = RecomendacionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['razon', 'obra__titulo']


class ObraVistaCacheViewSet(viewsets.ModelViewSet):
    queryset = ObraVistaCache.objects.all()
    serializer_class = ObraVistaCacheSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'genero', 'distrito', 'calle']

