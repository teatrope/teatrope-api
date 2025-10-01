from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BusquedaViewSet, RecomendacionViewSet, ObraVistaCacheViewSet

router = DefaultRouter()
router.register(r'busquedas', BusquedaViewSet)
router.register(r'recomendaciones', RecomendacionViewSet)
router.register(r'obras-cache', ObraVistaCacheViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

