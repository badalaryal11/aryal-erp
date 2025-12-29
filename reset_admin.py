
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
password = 'admin123'
email = 'admin@example.com'

try:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"SUCCESS: Created superuser '{username}' with password '{password}'")
    else:
        u = User.objects.get(username=username)
        u.set_password(password)
        u.save()
        print(f"SUCCESS: Updated password for existing user '{username}' to '{password}'")
except Exception as e:
    print(f"ERROR: {e}")
