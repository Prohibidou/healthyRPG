from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

# Mock user data
mock_user = {
    "username": "testuser",
    "password": "testpassword",
    "token": "mock-auth-token"
}

@csrf_exempt
def mock_login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if username == mock_user['username'] and password == mock_user['password']:
                return JsonResponse({'token': mock_user['token']})
            else:
                return JsonResponse({'non_field_errors': ['Unable to log in with provided credentials.']}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)
