from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.db.models import BooleanField, ExpressionWrapper, Q
import string
import secrets
import os

main_dir = "auth"
user_dir = "user"
avatar_dir = "avatar"


def get_avatar_path(instance, filename):
    return os.path.join(main_dir, user_dir, avatar_dir, filename)


class User(AbstractUser):
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(
        max_length=128, unique=True, blank=False, null=False
    )
    address = models.CharField(max_length=512, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True, null=True)


def get_random_digits():
    return get_random_string(length=6, allowed_chars="0123456789")


def get_expiration_date():
    return timezone.now() + timezone.timedelta(hours=6)


class ExpiredManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                expired=ExpressionWrapper(
                    Q(expiration_date__lt=timezone.now()), output_field=BooleanField()
                )
            )
        )


class ForgetRecord(models.Model):
    user = models.ForeignKey(
        "authentication.User", related_name="forget_records", on_delete=models.CASCADE
    )
    is_used = models.BooleanField(default=False)
    code = models.CharField(default=get_random_digits, max_length=6, editable=False)
    expiration_date = models.DateTimeField(default=get_expiration_date, editable=False)
    objects = ExpiredManager()


def get_verification_code():
    alphabet = string.hexdigits
    return ''.join(secrets.choice(alphabet) for i in range(32))

class VerificationCodeRecord(models.Model):
    user = models.OneToOneField(
        "authentication.User",
        on_delete=models.CASCADE,
        related_name="verification_record",
    )
    code = models.CharField(default=get_verification_code, max_length=32, editable=False)
    is_used = models.BooleanField(default=False)