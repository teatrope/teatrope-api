from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeatroViewSet, ObraViewSet, FuncionViewSet, PersonaViewSet

router = DefaultRouter()
router.register(r'teatros', TeatroViewSet)
router.register(r'obras', ObraViewSet)
router.register(r'funciones', FuncionViewSet)
router.register(r'personas', PersonaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

