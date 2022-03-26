from rest_framework import serializers
from shop.models import Order, Payment
from product.models import NightSkyProduct
from product.api.serializers import NightSkyProductSerializer


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("price", "is_verified", "ref_id")


class OrderSerializer(serializers.ModelSerializer):

    product = NightSkyProductSerializer(write_only=False, required=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ("id", "product", "payment", "status", "timestamp")

    def validate(self, attrs):
        # Just for now ;)
        return attrs

    def create(self, validated_data):
        user = self.context["request"].user
        
        product_data = validated_data.pop("product")
        product = NightSkyProduct.objects.create(**product_data)

        order = Order(
            product=product,
            user=user,
        )
        order.save()

        payment = Payment(order=order)
        payment.save()

        return order

