from django.db import models

from apps.shop.models import Shop


class Product(models.Model):
    """
    Product model

    Attributes:
        title (str): the title of the product
        desc (str): the description of the product
        image (img): the image of the product
        shops (FK): Many to Many relation to Shop model

    Methods:
        __str__(): returns title of the product
    """

    title = models.CharField(max_length=50, unique=True)
    desc = models.TextField(max_length=1000)
    image = models.ImageField(upload_to="products_images/", null=True)
    shops = models.ManyToManyField(Shop, through="ShopProduct", related_name="shops")

    def __str__(self):
        return f"{self.title}"


class ShopProduct(models.Model):
    """
    Supporting model for the Many to Many relation

    Attributes:
        shop (FK): the Foreign Key to Shop model
        product (FK): the Foreign Key to Product model
        price (int): the price of the product in the corresponding shop
        in_stock (int): the quantity of the products in the corresponding shop
    """

    shop = models.ForeignKey(
        Shop, on_delete=models.CASCADE, related_name="shopproducts"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="shopproducts"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField()


class Category(models.Model):
    """
    Category model

    Attributes:
        title (str): The title of the category
        parent (FK): A self-referential foreign key for category hierarchy
        products (FK): Many to Many relation to Product model

    Methods:
        __str__(): Returns the title of the category
    """

    title = models.CharField(max_length=30)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
    )
    products = models.ManyToManyField(Product, related_name="categories")

    def __str__(self):
        return f"{self.title}"

    def get_full_path(self):
        path = []
        category = self

        while category:
            path.append(category.title)
            category = category.parent

        return " > ".join(reversed(path))
