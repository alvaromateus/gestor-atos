"""buscaresolucoes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from ato.api import viewsets as atoviewsets
from django.conf.urls.static import static
from django.conf import settings
from ato import views


route = routers.DefaultRouter()
route.register(r'ato', atoviewsets.AtoViewSet, basename='Atos') 

urlpatterns = [
    path('api/', include(route.urls), name='api'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('get/ajax/assuntos', views.get_assuntos_secundarios, name="get_assuntos"),
    path('get/ajax/numero_documento', views.get_numero_documento, name="get_assuntos"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
