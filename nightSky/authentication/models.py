import black
from django.db import models
from django.contrib.auth.models import AbstractUser
import os

main_dir = "auth"
user_dir = "user"
avatar_dir = "avatar"


def get_avatar_path(instance, filename):
    return os.path.join(main_dir, user_dir, avatar_dir, filename)


class User(AbstractUser):
    phone_number = models.CharField(
        max_length=128, unique=True, blank=False, null=False
    )
    address = models.CharField(max_length=512, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True, null=True)
    
    # TODO: add verified field to user
