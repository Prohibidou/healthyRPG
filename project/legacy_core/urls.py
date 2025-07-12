from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from .auth_views import mock_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rpg/', include('rpg.urls', namespace='rpg')),
    path('pirate-view/', TemplateView.as_view(template_name='index.html'), name='pirate-view'),
    path('api-token-auth/', mock_login, name='api_token_auth'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
