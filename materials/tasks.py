from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from users.models import User


@shared_task
def update_alert(email, course):
    send_mail(
        subject='Платформа обучения',
        message=f'Обновился курс {course}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email]
    )


@shared_task
def user_deactivate():
    now = timezone.now()
    users_list = User.objects.all()

    for user in users_list:
        day_diff = (now - user.last_login).days
        if day_diff > 30:
            user.is_active = False
            user.save()
