from rest_framework import serializers
from .models import Busqueda, Recomendacion, ObraVistaCache


class ObraVistaCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObraVistaCache
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique cache ID'},
            'titulo': {'help_text': 'Play title'},
            'genero': {'help_text': 'Play genre'},
            'calle': {'help_text': 'Theater street'},
            'distrito': {'help_text': 'Theater district'},
            'latitud': {'help_text': 'Theater latitude'},
            'longitud': {'help_text': 'The theater longitude'},
            'funciones_json': {'help_text': 'JSON of associated functions'},
        }


class RecomendacionSerializer(serializers.ModelSerializer):
    busqueda = serializers.PrimaryKeyRelatedField(read_only=True, help_text='Associated search')
    obra = serializers.PrimaryKeyRelatedField(read_only=True, help_text='Recommended play')

    class Meta:
        model = Recomendacion
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique recommendation ID'},
            'busqueda': {'help_text': 'Associated search'},
            'obra': {'help_text': 'Recommended play'},
            'puntuacion': {'help_text': 'Recommendation score'},
            'razon': {'help_text': 'Reason for recommendation'},
        }


class BusquedaSerializer(serializers.ModelSerializer):
    recomendaciones = RecomendacionSerializer(many=True, read_only=True)

    class Meta:
        model = Busqueda
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique search ID'},
            'usuario_id': {'help_text': 'User ID'},
            'timestamp': {'help_text': 'Search timestamp'},
            'genero_filtro': {'help_text': 'Genre filter'},
            'calle_filtro': {'help_text': 'Street filter'},
            'distrito_filtro': {'help_text': 'District filter'},
            'latitud_filtro': {'help_text': 'Latitude filter'},
            'longitud_filtro': {'help_text': 'Longitude filter'},
            'fecha_inicio': {'help_text': 'Start date filter'},
            'fecha_fin': {'help_text': 'End date filter'},
        }

