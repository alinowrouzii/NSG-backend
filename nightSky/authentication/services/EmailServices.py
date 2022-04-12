from django.core.mail import BadHeaderError, send_mail
from rest_framework.exceptions import ValidationError
from nightSky.settings import EMAIL_HOST

def send_email(subject, message, to_email):

    try:
        send_mail(subject, message, EMAIL_HOST, [to_email])
        return True
    except BadHeaderError:
        raise ValidationError('Invalid header found.')
  