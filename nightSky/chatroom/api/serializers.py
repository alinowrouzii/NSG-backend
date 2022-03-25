from rest_framework import serializers
from chatroom.models import Message
from authentication.models import User
from shop.models import Order


class MessageSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=False,
        required=True,
    )

    order = serializers.PrimaryKeyRelatedField(
        queryset=Order.objects.all(),
        write_only=False,
        required=True,
    )
    
    class Meta:
        model = Message
        fields = (
            "user",
            "text",
            "photo",
            "order",
            "user_is_sender",
            "timestamp",
        )
        extra_kwargs = {
            "text": {"write_only": False, "required": True},
            "photo": {"write_only": False, "required": False},
            "user_is_sender": {"write_only": False, "required": True},
        }

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        message = Message.objects.create(**validated_data)

        return message
