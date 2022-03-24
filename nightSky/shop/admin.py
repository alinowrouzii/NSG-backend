from django.contrib import admin
from shop.models import Payment, Order
from django.forms import ModelForm, ValidationError


class OrderAdminForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

    def clean(self):
        cleaned_data = self.cleaned_data
        status = cleaned_data.get("status")
        if status == Order.StatusChoice.PAYMENT:
            payment = None
            try:
                payment = self.instance.payment
            except Payment.DoesNotExist:
                raise ValidationError("First create Payment and save order. Then change staus and save order again.")
            
            if payment.price == 0:
                raise ValidationError("First save the order with price greater than zero. Then change status to PAYMENT and save order again.")
           
        
        return cleaned_data


class PaymentInline(admin.StackedInline):
    model = Payment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_username",
        "get_user_fullname",
        "status",
        "get_payment_verified",
    )
    inlines = [PaymentInline]
    form = OrderAdminForm

    @admin.display(description="username")
    def get_username(self, obj):
        return obj.user.username

    @admin.display(description="fullname")
    def get_user_fullname(self, obj):
        return obj.user.get_full_name()

    @admin.display(description="payment verified")
    def get_payment_verified(self, obj):
        return obj.payment.is_verified


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "get_username", "get_user_fullname", "is_verified")

    @admin.display(description="username")
    def get_username(self, obj):
        return obj.order.user.username

    @admin.display(description="fullname")
    def get_user_fullname(self, obj):
        return obj.order.user.get_full_name()
