from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view # Import get_schema_view
from drf_yasg import openapi # Import openapi

router = DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Teatrope API",
        default_version='v1',
        description="API documentation for Teatrope, a theater discovery and ticketing platform.",
        terms_of_service="https://teatrope.github.io/teatrope-landing/en/",
        contact=openapi.Contact(email="contact@teatrope.com"), # Customize this email
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    schemes=['https'],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/', include('accounts.urls')),
        path('content/', include('content.urls')),
        path('discovery/', include('discovery.urls')),
        path('notifications/', include('notifications.urls')),
        path('tickets/', include('tickets.urls')),

        # Add Swagger/OpenAPI documentation URLs
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    ])),
]

