from django.db import models
from django.contrib.auth.models import AbstractBaseUser


ACCOUNT_TYPE_CHOICES = (
    ("SUPERUSER", "SUPERUSER"),
    ("RESP", "RESP"),  # RESPONSIBLE
)


class User(AbstractBaseUser):
    """
    Custom user model extending AbstractBaseUser.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email of the user.
        is_active (bool): Designates whether the user should be treated as active.
        role (str): The type of the account (RESPONSIBLE or SUPERUSER)

    Methods:
        full_name(): Returns the full name of the user.
        __str__(): Return the string representation of the user.
    """

    first_name = models.CharField(verbose_name="First name", max_length=30)
    last_name = models.CharField(verbose_name="Last name", max_length=40)
    email = models.EmailField(verbose_name="E-mail", unique=True)
    role = models.CharField(max_length=9, choices=ACCOUNT_TYPE_CHOICES, default="RESP")
    avatar = models.ImageField(
        upload_to="avatars/", null=True, default="avatars/default.jpg"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name
