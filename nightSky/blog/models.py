from email.policy import default
from django.db import models
from tinymce.models import HTMLField
from django.utils import timezone
from authentication.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
import jdatetime

import os

# Create your models here.


main_dir = "blog"
post_dir = "post"


def get_post_path(instance, filename):
    return os.path.join(main_dir, post_dir, filename)


# TODO: add db_index to timestamp fields
class Post(models.Model):
    title = models.CharField(max_length=1024, blank=False, null=False)
    description = HTMLField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)

    image = models.ImageField(upload_to=get_post_path, blank=True, null=True)

    def __str__(self):
        return f"{self.pk} | {self.title}"

    def get_jalali_date(self):
        return jdatetime.datetime.fromgregorian(
            date=timezone.localtime(self.timestamp), locale="fa_IR"
        ).strftime("%d %B %Y, ساعت %H:%M:00")


class Comment(models.Model):
    class StatusChoice(models.IntegerChoices):
        WAITING = 0, _("Waiting")
        ACCEPTED = 1, _("Accepted")
        REJECTED = 2, _("Rejected")

    text = models.CharField(max_length=256, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    score = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)], default=5
    )
    status = models.IntegerField(choices=StatusChoice.choices, default=0)

    def get_jalali_date(self):
        return jdatetime.datetime.fromgregorian(
            date=timezone.localtime(self.timestamp), locale="fa_IR"
        ).strftime("%d %B %Y, ساعت %H:%M:00")
