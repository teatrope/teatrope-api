from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsuarioViewSet

router = DefaultRouter()
router.register(r'users', UsuarioViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UsuarioViewSet.as_view({'post': 'register'})),
    path('token/login/', UsuarioViewSet.as_view({'post': 'login'})),
    path('token/logout/', UsuarioViewSet.as_view({'post': 'logout'})),
]

