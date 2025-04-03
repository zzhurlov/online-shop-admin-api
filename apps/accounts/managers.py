from django.contrib.auth.base_user import BaseUserManager
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("You must provide a valid email address")

    def validate_user(self, first_name, last_name, email):
        if not first_name:
            raise ValueError("You must provide a first name")

        if not last_name:
            raise ValueError("You must provide a last name")

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError("You must provide an email address!")

    def create_responsible(
        self, first_name, last_name, email, password, **extra_fields
    ):
        self.validate_user(first_name, last_name, email)

        user = self.model(
            first_name=first_name, last_name=last_name, email=email, **extra_fields
        )

        user.set_password(password)
        extra_fields.setdefault("role", "RESP")
        user.save()
        return user

    def validate_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("role", "SUPERUSER")

        if extra_fields.get("role") != "SUPERUSER":
            raise ValueError("Superusers must have superuser role!")

        if not password:
            raise ValueError("You must provide a password")

        if email:
            self.email_validator(email)
        else:
            raise ValueError("You must provide an email address")

        return extra_fields

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):
        extra_fields = self.validate_superuser(email, password, **extra_fields)
        user = self.create_responsible(
            first_name, last_name, email, password, **extra_fields
        )
        return user
