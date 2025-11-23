import os
import sys
import django
from django.core.management import call_command

def setup():
    print("=== HealthyRPG Project Setup ===\n")

    # 1. Setup Django Environment
    print("1. Configuring Django Environment...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legacy_core.settings')
    try:
        django.setup()
        print("   ✓ Django configured.\n")
    except Exception as e:
        print(f"   ❌ Error configuring Django: {e}")
        return

    # 2. Run Migrations
    print("2. Applying Database Migrations...")
    try:
        call_command('migrate')
        print("   ✓ Migrations applied.\n")
    except Exception as e:
        print(f"   ❌ Error applying migrations: {e}")
        return

    # 3. Configure Site
    print("3. Configuring Site Domain...")
    try:
        from django.contrib.sites.models import Site
        site, created = Site.objects.get_or_create(pk=1)
        site.domain = 'localhost:8000'
        site.name = 'localhost:8000'
        site.save()
        print(f"   ✓ Site configured as: {site.domain}\n")
    except Exception as e:
        print(f"   ❌ Error configuring Site: {e}")
        return

    # 4. Configure Google OAuth
    print("4. Configuring Google OAuth...")
    try:
        from allauth.socialaccount.models import SocialApp
        
        # Check if app exists
        app = SocialApp.objects.filter(provider='google').first()
        
        if app:
            print(f"   ✓ Found existing Google App: {app.name}")
            print(f"     Client ID: {app.client_id[:15]}...")
            update = input("   Do you want to update credentials? (y/n): ").lower().strip()
        else:
            print("   ⚠ No Google App found.")
            update = 'y'

        if update == 'y':
            print("   Please enter your Google Cloud Credentials:")
            client_id = input("   Client ID: ").strip()
            client_secret = input("   Client Secret: ").strip()

            if client_id and client_secret:
                if app:
                    app.client_id = client_id
                    app.secret = client_secret
                    app.save()
                    print("   ✓ Google OAuth app updated.")
                else:
                    app = SocialApp.objects.create(
                        provider='google',
                        name='Google OAuth',
                        client_id=client_id,
                        secret=client_secret
                    )
                    print("   ✓ Google OAuth app created.")
            else:
                print("   ⚠ Skipping update (empty credentials).")
        
        if app:
            app.sites.add(site)
            print("   ✓ Google OAuth app linked to site.\n")
            
    except Exception as e:
        print(f"   ❌ Error configuring Google OAuth: {e}")

    # 5. Create Superuser (Optional)
    print("5. Superuser Setup...")
    try:
        from django.contrib.auth.models import User
        if not User.objects.filter(is_superuser=True).exists():
            print("   No superuser found.")
            create = input("   Do you want to create a superuser? (y/n): ").lower().strip()
            if create == 'y':
                call_command('createsuperuser')
        else:
            print("   ✓ Superuser already exists.\n")
    except Exception as e:
        print(f"   ❌ Error checking/creating superuser: {e}")

    print("=== Setup Complete! ===")
    print("You can now run the server with: python manage.py runserver")

if __name__ == '__main__':
    setup()
