from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_payment_success_email_task(email_address):
    """
    celery task to send an email when payment is successfull
    """
    send_mail(
        subject='payment Successful',
        message='thank you for purchasing our product!',
        recipient_list=[email_address],
        from_email=settings.EMAIL_HOST_USER,
    )
