from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('rpg/', include('rpg.urls', namespace='rpg')),
    path('pirate-view/', TemplateView.as_view(template_name='index.html'), name='pirate-view'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^(?P<path>(?:favicon\.ico|manifest\.json|robots\.txt|logo(?:192|512)\.png))$',
                serve,
                {'document_root': settings.BASE_DIR / 'frontend' / 'build'}),
    ]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'frontend' / 'build')

urlpatterns += [
    re_path(r'^.*', TemplateView.as_view(template_name='index.html')),
]