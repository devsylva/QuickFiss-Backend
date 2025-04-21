from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task(bind=True, max_retries=3)
def send_otp_email(self, user_email, otp):
    try:
        subject = "Your OTP Verification Code" 
        send_mail(
            'OTP Verification',
            f'Your OTP is {otp}',
            settings.EMAIL_HOST_USER,
            [user_email],
            fail_silently=False,
        )
    except Exception as e:
        raise self.retry(exc=e, countdown=60)