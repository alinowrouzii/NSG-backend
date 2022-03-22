from rest_framework import serializers
from authentication.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

import re

# 4 MB
FILE_MAX_SIZE = 4 * 1000 * 1000
PHONE_REGEX = "(0?\d{10})"

def validate_avatar(image):
        print(image.name)
        print(image.size)
        if image.size > FILE_MAX_SIZE:
            print(image.size)
            raise ValidationError("File size is too big")
        
class UserSerializer(serializers.ModelSerializer):
    

    username = serializers.CharField(write_only=False, required=True,
                                     validators=[UniqueValidator(queryset=User.objects.all())],)
    phone_number = serializers.CharField(write_only=False, required=True,
                                         validators=[UniqueValidator(queryset=User.objects.all())],)
    password = serializers.CharField(write_only=True, required=True)
    password_verify = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=False, required=True)
    last_name = serializers.CharField(write_only=False, required=True)
    address = serializers.CharField(write_only=False, required=False)
    avatar = serializers.ImageField(
        write_only=False,
        required=False,
        validators=[validate_avatar],
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password_verify', 'phone_number',
                  'first_name', 'last_name', 'address', 'avatar')

    def validate(self, attrs):
        if self.context["request"].method == 'POST':
            if attrs["password"] != attrs["password_verify"]:
                raise ValidationError("Password is not match")
            print(attrs['phone_number'])
            # TODO regex does not work correctly
            if not re.search(PHONE_REGEX, attrs["phone_number"]):
                raise ValidationError("Phone number is not valid")

            return attrs
        elif self.context["request"].method == 'PATCH':
            # TODO
            return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data["phone_number"],
            address=validated_data.get("address", ""),
            avatar=validated_data.get("avatar", None),
        )

        user.set_password(validated_data["password"])

        user.save()
        return user
