from rest_framework import serializers
from .models import Busqueda, Recomendacion, ObraVistaCache


class ObraVistaCacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObraVistaCache
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique cache ID (UUID)'},
            'titulo': {'help_text': 'Play title'},
            'genero': {'help_text': 'Play genre (e.g., DRAMA, COMEDIA)'},
            'calle': {'help_text': 'Street address'},
            'distrito': {'help_text': 'District'},
            'latitud': {'help_text': 'Latitude coordinate'},
            'longitud': {'help_text': 'Longitude coordinate'},
            'funciones_json': {'help_text': 'JSON of functions'},
        }


class RecomendacionSerializer(serializers.ModelSerializer):
    busqueda = serializers.PrimaryKeyRelatedField(queryset=Busqueda.objects.all(), help_text='ID of the associated search (UUID)')
    obra = serializers.PrimaryKeyRelatedField(queryset=ObraVistaCache.objects.all(), help_text='ID of the recommended play cache (UUID)')

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

    def validate_busqueda(self, value):
        return value

    def validate_obra(self, value):
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Only nest ObraVistaCacheSerializer to avoid circular dependency
        # The 'busqueda' field will be represented by its PK (UUID) by default
        representation['obra'] = ObraVistaCacheSerializer(instance.obra).data
        return representation


class BusquedaSerializer(serializers.ModelSerializer):
    recomendaciones = RecomendacionSerializer(many=True, read_only=True)

    class Meta:
        model = Busqueda
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique search ID (UUID)'},
            'usuario_id': {'help_text': 'User ID (UUID)'},
            'timestamp': {'help_text': 'Search timestamp'},
            'genero_filtro': {'help_text': 'Genre filter (e.g., DRAMA)'},
            'calle_filtro': {'help_text': 'Street filter'},
            'distrito_filtro': {'help_text': 'District filter'},
            'latitud_filtro': {'help_text': 'Latitude filter'},
            'longitud_filtro': {'help_text': 'Longitude filter'},
            'fecha_inicio': {'help_text': 'Start date filter'},
            'fecha_fin': {'help_text': 'End date filter'},
            'recomendaciones': {'help_text': 'List of recommendations for this search'},
        }

