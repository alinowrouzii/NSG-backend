from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Order(models.Model):
    class StatusChoice(models.IntegerChoices):
        PENDING = 0, _("Pending")
        ACCEPTED = 1, _("Accepted")
        PAYMENT = 2, _("Payment")
        POSTING = 3, _("Posting")
        POSTED = 4, _("Posted")
    
    product = models.OneToOneField("product.NightSkyProduct", on_delete=models.CASCADE, null=True, related_name="orders")
    user = models.ForeignKey("authentication.User", on_delete=models.SET_NULL, null=True, related_name="orders")
    status = models.IntegerField(choices=StatusChoice.choices, default=StatusChoice.PENDING)
    timestamp = models.DateTimeField(default=timezone.now, editable=False)
    
    def __str__(self):
        pass
        return f"{self.id} | {self.user.username}"
    
    
    
    
class Payment(models.Model):
    price = models.PositiveIntegerField(default=0, help_text="At the payment stage, the price should be greather than zero")
    is_verified = models.BooleanField(default=False)
    order = models.OneToOneField("shop.Order", on_delete=models.CASCADE, related_name="payment")
    
    authority = models.CharField(max_length=512, blank=True)
    ref_id = models.CharField(max_length=512, blank=True)
    


@receiver(pre_save, sender=Order)
def my_callback(sender, instance, *args, **kwargs):
    # Reverse relation from model to OneToOne field
    try:
        payment = instance.payment
        if payment.price == 0 and instance.status == Order.StatusChoice.PAYMENT:
            raise ValidationError({"order_price": "Price should be set for payment stage"})
    except Payment.DoesNotExist:
        pass        
