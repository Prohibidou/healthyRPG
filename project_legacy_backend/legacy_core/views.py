from django.shortcuts import redirect
from rest_framework.authtoken.models import Token
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login

def google_login_callback(request):
    adapter = GoogleOAuth2Adapter(request)
    app = adapter.get_provider().get_app(request)
    client = adapter.get_client(request, app)
    access_token = client.get_access_token(request.GET['code'])
    social_login = adapter.complete_login(request, app, access_token)
    social_login.user.save()
    complete_social_login(request, social_login)
    token, created = Token.objects.get_or_create(user=social_login.user)
    return redirect(f'http://localhost:3000/auth/callback?token={token.key}')
