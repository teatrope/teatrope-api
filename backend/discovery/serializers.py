from rest_framework import serializers
from .models import Busqueda, Recomendacion, ObraVistaCache


class ObraVistaCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObraVistaCache
        fields = '__all__'


class RecomendacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recomendacion
        fields = '__all__'


class BusquedaSerializer(serializers.ModelSerializer):
    recomendaciones = RecomendacionSerializer(many=True, read_only=True)

    class Meta:
        model = Busqueda
        fields = '__all__'

