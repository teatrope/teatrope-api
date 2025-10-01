from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id', 'email', 'tipo_rol', 'permisos_json', 'generos_preferidos_json',
            'calle_preferida', 'distrito_preferida', 'latitud_preferida', 'longitud_preferida'
        ]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'password', 'tipo_rol']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password')
        attrs['user'] = user
        return attrs

