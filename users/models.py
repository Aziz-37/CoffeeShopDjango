from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, default='user')
    is_verified = models.BooleanField(default=False)

    @classmethod
    def delete_unverified_users(cls):
        two_days_ago = timezone.now() - timezone.timedelta(days=2)
        cls.objects.filter(is_verified=False, created_at__lte=two_days_ago).delete()


    def __str__(self):
        return self.username