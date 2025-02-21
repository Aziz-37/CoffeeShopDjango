from celery import shared_task
from django.core.management import call_command

@shared_task
def delete_unverified_users():
    call_command('delete_unverified_users')
