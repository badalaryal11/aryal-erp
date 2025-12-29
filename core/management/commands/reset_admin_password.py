from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Resets the admin password to default'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = 'admin'
        password = 'admin123'
        email = 'admin@example.com'

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f"Created superuser '{username}'"))
        else:
            u = User.objects.get(username=username)
            u.set_password(password)
            u.save()
            self.stdout.write(self.style.SUCCESS(f"Updated password for '{username}'"))
        
        self.stdout.write(self.style.WARNING(f"Password set to: {password}"))
