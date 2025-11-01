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
        extra_kwargs = {
            'id': {'help_text': 'Unique user ID'},
            'email': {'help_text': 'User email address'},
            'tipo_rol': {'help_text': 'User role type'},
            'permisos_json': {'help_text': 'JSON of user permissions'},
            'generos_preferidos_json': {'help_text': 'JSON of preferred genres'},
            'calle_preferida': {'help_text': 'Preferred street'},
            'distrito_preferida': {'help_text': 'Preferred district'},
            'latitud_preferida': {'help_text': 'Preferred latitude'},
            'longitud_preferida': {'help_text': 'Preferred longitude'},
        }


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8, help_text="Password (minimum 8 characters)")

    class Meta:
        model = Usuario
        fields = ['id', 'email', 'password', 'tipo_rol']
        extra_kwargs = {
            'email': {'help_text': 'User email address'},
            'tipo_rol': {'help_text': 'User role type'},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = Usuario.objects.create_user(password=password, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text="User email")
    password = serializers.CharField(write_only=True, help_text="User password")

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid email or password')
        attrs['user'] = user
        return attrs

