"""
Script para configurar Google OAuth Social App en Django
Ejecutar: python setup_google_oauth.py
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legacy_core.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def setup_google_oauth():
    print("=== Configuración de Google OAuth ===\n")
    
    # Get or create site
    site, created = Site.objects.get_or_create(
        pk=1,
        defaults={
            'domain': 'localhost:8000',
            'name': 'localhost:8000'
        }
    )
    
    if created:
        print(f"✓ Site creado: {site.domain}")
    else:
        print(f"✓ Site existente: {site.domain}")
        # Update if needed
        if site.domain != 'localhost:8000':
            site.domain = 'localhost:8000'
            site.name = 'localhost:8000'
            site.save()
            print("  → Actualizado a localhost:8000")
    
    # Check if Google social app exists
    try:
        app = SocialApp.objects.get(provider='google')
        print(f"\n⚠ Ya existe una aplicación de Google OAuth")
        print(f"  Client ID: {app.client_id[:20]}..." if app.client_id else "  Client ID: (vacío)")
        print(f"  Secret: {'***configurado***' if app.secret else '(vacío)'}")
        
        update = input("\n¿Deseas actualizarla? (s/n): ").lower().strip()
        if update != 's':
            print("\nCancelado. No se realizaron cambios.")
            return
    except SocialApp.DoesNotExist:
        app = None
    
    # Get credentials from user
    print("\n--- Ingresa tus credenciales de Google Cloud Console ---")
    print("Si no las tienes, sigue las instrucciones en walkthrough.md\n")
    
    client_id = input("Client ID: ").strip()
    if not client_id:
        print("❌ Error: Client ID no puede estar vacío")
        return
    
    secret = input("Client Secret: ").strip()
    if not secret:
        print("❌ Error: Client Secret no puede estar vacío")
        return
    
    # Create or update social app
    if app:
        app.client_id = client_id
        app.secret = secret
        app.save()
        print("\n✓ Aplicación de Google OAuth actualizada")
    else:
        app = SocialApp.objects.create(
            provider='google',
            name='Google OAuth',
            client_id=client_id,
            secret=secret
        )
        app.sites.add(site)
        print("\n✓ Aplicación de Google OAuth creada")
    
    # Verify configuration
    print("\n=== Configuración Completa ===")
    print(f"Provider: {app.provider}")
    print(f"Name: {app.name}")
    print(f"Client ID: {app.client_id[:20]}...")
    print(f"Secret: ***configurado***")
    print(f"Sites: {', '.join([s.domain for s in app.sites.all()])}")
    
    print("\n✅ Todo listo! Ahora puedes probar el login con Google")
    print("\nPasos siguientes:")
    print("1. Inicia el servidor: python manage.py runserver")
    print("2. Inicia el frontend: cd frontend && npm start")
    print("3. Ve a http://localhost:3000/login")
    print("4. Haz clic en 'Login with Google'")
    
    print("\n⚠ IMPORTANTE: Asegúrate de haber configurado el URI de redirección en Google Cloud Console:")
    print("   http://localhost:8000/accounts/google/login/callback/")

if __name__ == '__main__':
    try:
        setup_google_oauth()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
