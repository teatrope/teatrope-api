from rest_framework import serializers
from .models import Teatro, Obra, Funcion, Persona


class TeatroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teatro
        fields = '__all__'


class ObraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obra
        fields = '__all__'


class FuncionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcion
        fields = '__all__'


class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

