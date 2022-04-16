from django.core.mail import BadHeaderError, send_mail
from rest_framework.exceptions import ValidationError
from nightSky.settings import EMAIL_HOST

def send_email(subject, message, to_email):

    try:
        # send_mail(subject, message, EMAIL_HOST, [to_email])
        pass
    except BadHeaderError:
        raise ValidationError('Invalid header found.')
    except Exception:
        raise ValidationError('Fail to send email.')
        
  
  
  
def send_verification_code(*args, **kwargs):
    verification_record = kwargs.pop("verification_record")
    message = f"Here is your verification code: {verification_record.code}"
    send_email(message=message, subject="subject", to_email=verification_record.user.email)
    
    