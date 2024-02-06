from django.core.management import BaseCommand

from users.models import User
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email=settings.EMAIL_SUPERUSER,
            first_name='Admin',
            last_name='Adminov',
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )

        user.set_password(settings.PASS_SUPERUSER)
        user.save()
