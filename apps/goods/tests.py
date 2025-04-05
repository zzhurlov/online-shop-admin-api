from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from apps.goods.models import Product, ShopProduct, Category
from apps.goods.serializers import ProductSerializer, CategorySerializer
from apps.shop.models import Shop
from apps.accounts.models import User


# Models
class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            title="Test Product", desc="A product description"
        )

    def test_product_str_method(self):
        self.assertEqual(str(self.product), "Test Product")


class CategoryModelTest(TestCase):
    def setUp(self):
        self.parent = Category.objects.create(title="Electronics")
        self.child = Category.objects.create(title="Phones", parent=self.parent)

    def test_category_str_method(self):
        self.assertEqual(str(self.child), "Phones")

    def test_category_get_full_path(self):
        path = self.child.get_full_path()
        self.assertEqual(path, "Electronics > Phones")


# Serializers
class ProductSerializerTest(TestCase):
    def test_product_serializer_data(self):
        product = Product.objects.create(title="Serialized Product", desc="Desc")
        serializer = ProductSerializer(product)
        self.assertEqual(serializer.data["title"], "Serialized Product")


class CategorySerializerTest(TestCase):
    def test_category_full_path(self):
        parent = Category.objects.create(title="Books")
        child = Category.objects.create(title="Fiction", parent=parent)
        serializer = CategorySerializer(child)
        self.assertEqual(serializer.data["full_path"], "Books > Fiction")


# Views
class GoodsAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_responsible(
            first_name="test",
            last_name="testov",
            email="test@example.com",
            password="pass1234",
        )
        self.client.force_authenticate(user=self.user)

        self.shop = Shop.objects.create(
            title="Test Shop", image="http://test.com/image.jpg"
        )
        self.product = Product.objects.create(title="API Product", desc="Some product")
        self.shopproduct = ShopProduct.objects.create(
            shop=self.shop, product=self.product, price=199.99, in_stock=10
        )
        self.category = Category.objects.create(title="Gadgets")

    def test_get_products_list(self):
        url = reverse("products")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("API Product", str(response.data))

    def test_create_product(self):
        url = reverse("products")
        payload = {
            "product": {"title": "New API Product", "desc": "Test Desc", "image": None},
            "shop": self.shop.id,
            "price": 123.45,
            "in_stock": 5,
        }
        response = self.client.post(url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"]["title"], "New API Product")

    def test_get_product_by_id(self):
        url = reverse("product", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["product"]["title"], "API Product")

    def test_patch_product(self):
        url = reverse("product", args=[self.product.id])
        response = self.client.patch(url, {"price": 888.88}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data["price"]), 888.88)

    def test_get_categories(self):
        url = reverse("categories")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Gadgets", str(response.data))

    def test_create_category(self):
        url = reverse("categories")
        response = self.client.post(
            url, {"title": "Accessories", "products": [self.product.id]}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Accessories")

    def test_get_category_by_id(self):
        url = reverse("category", args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Gadgets")
