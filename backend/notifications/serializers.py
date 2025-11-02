from rest_framework import serializers
from .models import Notificacion, RecomendacionPersonalizada, PreferenciasUsuario


class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique notification ID (UUID)'},
            'usuario_id': {'help_text': 'User ID (UUID)'},
            'tipo': {'help_text': 'Notification type (e.g., ESTRENO)'},
            'contenido': {'help_text': 'Notification content'},
            'timestamp': {'help_text': 'Notification timestamp'},
            'estado': {'help_text': 'Notification status (e.g., ENVIADA)'},
            'titulo_mensaje': {'help_text': 'Message title'},
            'cuerpo_mensaje': {'help_text': 'Message body'},
            'enlace_mensaje': {'help_text': 'Message link'},
        }


class RecomendacionPersonalizadaSerializer(serializers.ModelSerializer):
    notificacion = serializers.PrimaryKeyRelatedField(queryset=Notificacion.objects.all(), help_text='ID of the associated notification (UUID)')

    class Meta:
        model = RecomendacionPersonalizada
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'Unique personalized recommendation ID (UUID)'},
            'obra_id': {'help_text': 'Play ID (UUID)'},
            'score_relevancia': {'help_text': 'Relevance score'},
            'razon': {'help_text': 'Reason for recommendation'},
        }

    def validate_notificacion(self, value):
        return value

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Nest the related notification object for read operations
        representation['notificacion'] = NotificacionSerializer(instance.notificacion).data
        return representation


class PreferenciasUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreferenciasUsuario
        fields = '__all__'
        extra_kwargs = {
            'usuario_id': {'help_text': 'User ID (UUID)'},
            'generos_json': {'help_text': 'JSON of preferred genres'},
            'calle_preferida': {'help_text': 'Preferred street'},
            'distrito_preferida': {'help_text': 'Preferred district'},
            'latitud_preferida': {'help_text': 'Preferred latitude'},
            'longitud_preferida': {'help_text': 'Preferred longitude'},
            'frecuencia_notif': {'help_text': 'Notification frequency (e.g., DIARIA)'},
        }

