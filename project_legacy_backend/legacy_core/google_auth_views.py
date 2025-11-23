from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from rest_framework.authtoken.models import Token


@login_required
def google_callback(request):
    """
    Handle Google OAuth callback and redirect to frontend with token
    """
    # Get or create token for the user
    token, created = Token.objects.get_or_create(user=request.user)
    
    # Redirect to frontend callback with token
    frontend_callback_url = f'http://localhost:3001/auth/callback?token={token.key}'
    return redirect(frontend_callback_url)
