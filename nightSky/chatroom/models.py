from django.db import models
from django.utils import timezone
import os

main_dir = "chatroom"
message_dir = "message"
user_dir = "user"


def get_message_path(instance, filename):
    return os.path.join(
        main_dir, message_dir, user_dir, str(instance.user.id), filename
    )


class Message(models.Model):

    user = models.ForeignKey(
        "authentication.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="user_messages",
    )
    user_is_sender = models.BooleanField(default=False)
    
    order = models.ForeignKey(
        "shop.Order",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_messages",
    )
    text = models.CharField(max_length=1024, blank=False, null=False)
    photo = models.ImageField(upload_to=get_message_path, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
