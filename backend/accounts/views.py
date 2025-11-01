from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .models import Usuario
from .serializers import UsuarioSerializer, RegisterSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all().order_by('email')
    serializer_class = UsuarioSerializer

    def get_permissions(self):
        if self.action in ['register', 'login']:
            return [AllowAny()]
        return super().get_permissions()

    @swagger_auto_schema(
        method='post',
        request_body=RegisterSerializer,
        responses={201: openapi.Response('User registered with token', UsuarioSerializer)}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'user': UsuarioSerializer(user).data, 'token': token.key}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        method='post',
        request_body=LoginSerializer,
        responses={200: openapi.Response('Login successful with token', UsuarioSerializer)}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UsuarioSerializer(user).data})

    @swagger_auto_schema(
        method='post',
        responses={204: 'Logout successful'}
    )
    @action(detail=False, methods=['post'])
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

