from django.shortcuts import redirect
from rest_framework.authtoken.models import Token

def google_login_callback(request):
    print(f"User logged in: {request.user.username}, email: {request.user.email}")
    token, created = Token.objects.get_or_create(user=request.user)
    return redirect(f'http://localhost:8000/auth/callback?token={token.key}')
