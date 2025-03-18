from django.db import models
from apps.accounts.models import User


class Shop(models.Model):
    """
    Shop model

    Attributes:
        title (str): the title of the shop
        desc (str): the description of the shop
        responsible_id (FK): the foreign key to responsible for this shop
        is_active (bool): Indicates whether the store is active
        image (img): The image of the shop

    Methods:
        __str__(): Returns the title of the shop for recognition
    """

    title = models.CharField(max_length=30)
    desc = models.TextField(max_length=1000)
    responsible_id = models.ManyToManyField(User)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="shops_images/")

    def __str__(self):
        return f"{self.title}"
