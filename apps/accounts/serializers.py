from rest_framework import serializers
from apps.accounts.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class ResponsibleSerializer(serializers.ModelSerializer):
    """
    This serializer needs for serialization
    responsibles of shops at /shops/ endpoint
    """

    class Meta:
        model = User
        exclude = ["last_login", "password", "is_staff", "avatar"]
