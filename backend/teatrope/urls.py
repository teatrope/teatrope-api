from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/', include('accounts.urls')),
        path('content/', include('content.urls')),
        path('discovery/', include('discovery.urls')),
        path('notifications/', include('notifications.urls')),
        path('tickets/', include('tickets.urls')),
    ])),
]

