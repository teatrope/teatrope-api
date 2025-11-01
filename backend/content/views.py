from rest_framework import viewsets
from rest_framework import filters
from .models import Teatro, Obra, Funcion, Persona
from .serializers import TeatroSerializer, ObraSerializer, FuncionSerializer, PersonaSerializer


class TeatroViewSet(viewsets.ModelViewSet):
    queryset = Teatro.objects.all()
    serializer_class = TeatroSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'distrito', 'calle']


class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.select_related('teatro').all()
    serializer_class = ObraSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'genero', 'director_nombre', 'teatro__nombre']


class FuncionViewSet(viewsets.ModelViewSet):
    queryset = Funcion.objects.select_related('obra').all()
    serializer_class = FuncionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['obra__titulo']


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.select_related('obra').all()
    serializer_class = PersonaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre_completo', 'rol', 'obra__titulo']
