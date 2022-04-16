from rest_framework import serializers
from authentication.models import User, VerificationCodeRecord
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from authentication.models import ForgetRecord
from authentication.services.EmailServices import send_verification_code
from django.db import transaction

import re

# 4 MB
FILE_MAX_SIZE = 4 * 1000 * 1000
PHONE_REGEX = "^09[\d]{9}$"


def validate_avatar(image):
    print(image.name)
    print(image.size)
    if image.size > FILE_MAX_SIZE:
        print(image.size)
        raise ValidationError("File size is too big")


class UserSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        write_only=False,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    phone_number = serializers.CharField(
        write_only=False,
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
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
        fields = (
            "username",
            "password",
            "password_verify",
            "phone_number",
            "first_name",
            "last_name",
            "address",
            "avatar",
            "email",
            "id",
        )

    def validate(self, attrs):
        if self.context["request"].method == "POST":
            if attrs["password"] != attrs["password_verify"]:
                raise ValidationError({"password": "Password is not match"})

            # TODO regex does not work correctly
            if not re.search(PHONE_REGEX, attrs["phone_number"]):
                raise ValidationError({"phone_number": "Phone number is not valid"})
            return attrs

        # PATCH method
        try:
            if not re.search(PHONE_REGEX, attrs["phone_number"]):
                raise ValidationError({"phone_number": "Phone number is not valid"})
        except KeyError:
            pass

        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            user = User(
                username=validated_data["username"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                phone_number=validated_data["phone_number"],
                address=validated_data.get("address", ""),
                email=validated_data.get("email", ""),
                avatar=validated_data.get("avatar", None),
            )

            user.set_password(validated_data["password"])
            user.save()
            
            
            # create verification record here
            verification_record = VerificationCodeRecord.objects.create(user=user)
            send_verification_code(verification_record=verification_record)    

            return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.address = validated_data.get("address", instance.address)
        instance.email = validated_data.get("email", instance.email)
        instance.avatar = validated_data.get("avatar", instance.avatar)

        instance.save()

        return instance

class UserVerifySerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True, write_only=True)
    
    class Meta:
        model = User
        fields = ("code", "username")
        extra_kwargs = {
            "username": {
                "read_only": True
            }
        }
        
    def update(self, instance, validated_data):
        code = validated_data["code"]
        
        try:
            verification_record = VerificationCodeRecord.objects.get(is_used=False, code=code)
            verification_record.is_used = True
            verification_record.save()
            
            user = verification_record.user
            user.is_verified = True
            user.save()
            
            return user
        except VerificationCodeRecord.DoesNotExist:
            raise ValidationError({"detail": "code is not valid"})
    
class UserSerializerMinimal(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True, source="get_full_name")

    class Meta:
        model = User
        fields = ("full_name", "avatar")


class ForgetPasswordRequestSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=True,
        write_only=True,
    )

    class Meta:
        model = ForgetRecord
        fields = ("user", "code", "expiration_date")

    def validate(self, attrs):
        return super().validate(attrs)

    def create(self, validated_data):
        return ForgetRecord.objects.create(**validated_data)


class ForgetPasswordVerifySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    code = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = ForgetRecord
        fields = ("code", "user", "new_password")

    def validate(self, attrs):
        return super().validate(attrs)

    def update(self, instance, validated_data):
        with transaction.atomic():
            user = instance.user
            user.set_password(validated_data["new_password"])
            user.save()

            instance.is_used = True
            instance.save()

        return instance



class VerificationCodeRecordSerializer(serializers.ModelSerializer):
    
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        required=True
    )
    
    class Meta:
        model = VerificationCodeRecord
        fields = ("user",)
        
    def validated_data(self):
        return super().validated_data
    
    def create(self, validated_data):
        verification_record = VerificationCodeRecord.objects.create(user=validated_data["user"])
        # send_verification_code(verification_record.user)    
        return verification_record
    
    def update(self, instance, validated_data):
        user = instance.user
        user.is_verified=True
        user.save()
        return instance