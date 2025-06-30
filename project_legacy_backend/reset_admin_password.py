from django.contrib.auth.models import User
try:
    user = User.objects.get(username='admin')
    user.set_password('admin')
    user.save()
    print("Admin password has been reset successfully.")
except User.DoesNotExist:
    print("User 'admin' not found.")
