from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Удаляет пользователей, не прошедших верификацию более 2 дней'

    def handle(self, *args, **options):
        threshold = timezone.now() - timedelta(days=2)
        unverified_users = User.objects.filter(is_verified=False, date_joined__lt=threshold)
        count = unverified_users.count()
        unverified_users.delete()
        self.stdout.write(self.style.SUCCESS(f'Удалено {count} не верифицированных пользователей'))
