from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet, DetalleEntradaViewSet, DisponibilidadCacheViewSet

router = DefaultRouter()
router.register(r'reservas', ReservaViewSet)
router.register(r'detalles', DetalleEntradaViewSet)
router.register(r'disponibilidad', DisponibilidadCacheViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

