from rest_framework import viewsets
from .models import Teatro, Obra, Funcion, Persona
from .serializers import TeatroSerializer, ObraSerializer, FuncionSerializer, PersonaSerializer


class TeatroViewSet(viewsets.ModelViewSet):
    queryset = Teatro.objects.all()
    serializer_class = TeatroSerializer


class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.select_related('teatro').all()
    serializer_class = ObraSerializer


class FuncionViewSet(viewsets.ModelViewSet):
    queryset = Funcion.objects.select_related('obra').all()
    serializer_class = FuncionSerializer


class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.select_related('obra').all()
    serializer_class = PersonaSerializer

