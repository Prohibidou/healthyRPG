# legacy_core/urls.py
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework.authtoken.views import obtain_auth_token

def home(request):
    return HttpResponse(" Bienvenido a Project Legacy API, hermoso señor que visita por primera vez este sitio", content_type="text/html")

urlpatterns = [
    path('',               home),                     # ← ruta raiz
    path('admin/',         admin.site.urls),
    path('api/',           include('rpg.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]
