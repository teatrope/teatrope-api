from rest_framework import serializers
from .models import Teatro, Obra, Funcion, Persona


class TeatroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teatro
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique theater ID'},
            'nombre': {'help_text': 'Theater name'},
            'descripcion': {'help_text': 'Theater description'},
            'calle': {'help_text': 'Theater street'},
            'distrito': {'help_text': 'Theater district'},
            'latitud': {'help_text': 'Theater latitude'},
            'longitud': {'help_text': 'The theater longitude'},
        }


class ObraSerializer(serializers.ModelSerializer):
    teatro = TeatroSerializer(read_only=True)

    class Meta:
        model = Obra
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique play ID'},
            'teatro': {'help_text': 'Associated theater'},
            'titulo': {'help_text': 'Play title'},
            'genero': {'help_text': 'Play genre'},
            'director_nombre': {'help_text': 'Director name'},
            'director_rol': {'help_text': 'Director role'},
        }


class FuncionSerializer(serializers.ModelSerializer):
    obra = ObraSerializer(read_only=True)

    class Meta:
        model = Funcion
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique function ID'},
            'obra': {'help_text': 'Associated play'},
            'fecha': {'help_text': 'Function date and time'},
            'duracion_minutos': {'help_text': 'Function duration in minutes'},
            'disponibilidad_asientos': {'help_text': 'Number of available seats'},
        }


class PersonaSerializer(serializers.ModelSerializer):
    obra = ObraSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique person ID'},
            'obra': {'help_text': 'Associated play'},
            'nombre_completo': {'help_text': 'Person name'},
            'rol': {'help_text': 'Person role'},
        }