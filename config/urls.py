from django.contrib import admin
from django.urls import path,include
from django.urls import re_path as url
from django.conf.urls.static import static
from django.conf import settings
from news.api import NewsViewSet, CategoryViewSet
from rest_framework import routers, serializers, viewsets

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'news', NewsViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    url(r'^auth/', include('djoser.urls')),
    url(r'^auth/', include('djoser.urls.authtoken')),
    path('api-auth/', include('rest_framework.urls')),
    url('', include('news.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)