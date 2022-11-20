from django.core.management.base import BaseCommand
from backend.user_profile.models import *


class Command(BaseCommand):
    """
    Create a superuser if none exist
    Example:
        manage.py createsuperuser_if_none_exists --user=admin --password=changeme
    """

    def add_arguments(self, parser):
        parser.add_argument("--user", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="admin@example.com")

    def handle(self, *args, **options):
        if User.objects.filter(username='admin').exists():
            self.stdout.write(f'Superuser already exists')
            return
        username = options["user"]
        password = options["password"]
        email = options["email"]
        User.objects.create_superuser(username=username, password=password, email=email)
        self.stdout.write(f'Superuser "{username}" was created')