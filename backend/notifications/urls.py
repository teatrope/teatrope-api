from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificacionViewSet, RecomendacionPersonalizadaViewSet, PreferenciasUsuarioViewSet

router = DefaultRouter()
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'recomendaciones-personalizadas', RecomendacionPersonalizadaViewSet)
router.register(r'preferencias', PreferenciasUsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

