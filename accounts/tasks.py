from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def sendemail(subject, html_text, to_email):
    send_mail(
        subject=subject,
        message='',
        html_message=html_text,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[to_email],
        fail_silently=False,
    )