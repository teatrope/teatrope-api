import uuid
from rest_framework import serializers
from .models import Teatro, Obra, Funcion, Persona


class TeatroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teatro
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique theater ID (UUID)'},
            'nombre': {'help_text': 'Theater name'},
            'descripcion': {'help_text': 'Theater description'},
            'calle': {'help_text': 'Street address'},
            'distrito': {'help_text': 'District'},
            'latitud': {'help_text': 'Latitude coordinate'},
            'longitud': {'help_text': 'Longitude coordinate'},
        }


class ObraSerializer(serializers.ModelSerializer):
    teatro = serializers.UUIDField(help_text='ID of the associated theater (UUID)')

    class Meta:
        model = Obra
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique play ID (UUID)'},
            'titulo': {'help_text': 'Play title'},
            'genero': {'help_text': 'Play genre (e.g., DRAMA, COMEDIA)'},
            'director_nombre': {'help_text': 'Director name'},
            'director_rol': {'help_text': 'Director role (e.g., DIRECTOR)'},
        }

    def validate_teatro(self, value):
        try:
            value = uuid.UUID(str(value))  # Ensure it's a valid UUID
        except ValueError:
            raise serializers.ValidationError("Invalid UUID format for theater ID.")
        if not Teatro.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid theater ID - no matching theater found.")
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['teatro'] = TeatroSerializer(instance.teatro).data  # Nest for read
        return representation


class FuncionSerializer(serializers.ModelSerializer):
    obra = ObraSerializer(read_only=True)

    class Meta:
        model = Funcion
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique function ID (UUID)'},
            'obra': {'help_text': 'Associated play'},
            'fecha': {'help_text': 'Function date and time'},
            'duracion_minutos': {'help_text': 'Duration in minutes'},
            'disponibilidad_asientos': {'help_text': 'Available seats'},
        }


class PersonaSerializer(serializers.ModelSerializer):
    obra = ObraSerializer(read_only=True)

    class Meta:
        model = Persona
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique person ID (UUID)'},
            'obra': {'help_text': 'Associated play'},
            'nombre_completo': {'help_text': 'Full name'},
            'rol': {'help_text': 'Role (e.g., ACTOR, DIRECTOR)'},
        }