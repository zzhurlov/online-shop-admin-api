from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

from apps.shop.models import Shop
from apps.accounts.models import User
from apps.shop.serializers import ShopSerializer


# Models
class ShopModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_responsible(
            first_name="test",
            last_name="test",
            email="test1@test.ru",
            password="testpass",
        )
        self.shop = Shop.objects.create(
            title="Tech World", desc="Best electronics", is_active=True
        )
        self.shop.responsible_id.add(self.user)

    def test_shop_str(self):
        self.assertEqual(str(self.shop), "Tech World")

    def test_shop_responsible(self):
        self.assertIn(self.user, self.shop.responsible_id.all())


# Serializers
class ShopSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_responsible(
            first_name="test",
            last_name="test",
            email="test3@test.ru",
            password="testpass",
        )
        self.shop = Shop.objects.create(title="Shop A", desc="Description A")
        self.shop.responsible_id.add(self.user)

    def test_shop_serializer_data(self):
        serializer = ShopSerializer(self.shop)
        data = serializer.data

        self.assertEqual(data["title"], "Shop A")
        self.assertEqual(data["desc"], "Description A")
        self.assertTrue("responsible_id" in data)


# Views
class ShopViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.superuser = User.objects.create_superuser(
            first_name="test1",
            last_name="test2",
            email="test2@test.ru",
            password="testpass",
        )
        self.user = User.objects.create_responsible(
            first_name="test",
            last_name="test",
            email="test4@test.ru",
            password="testpass",
        )

        self.shop = Shop.objects.create(
            title="Cool Store", desc="Nice stuff", is_active=True
        )
        self.shop.responsible_id.add(self.superuser)

        self.shops_url = reverse("shops")
        self.shop_detail_url = reverse("shop", args=[self.shop.id])

    def test_get_shops_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.shops_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_get_shop_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.shop_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Cool Store")

    def test_create_shop_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)

        payload = {
            "title": "Super Shop",
            "desc": "Mega description",
            "responsible_id": [self.superuser.id],
            "is_active": True,
        }

        response = self.client.post(self.shops_url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Super Shop")

    def test_create_shop_as_regular_user_forbidden(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "title": "Hacker Shop",
            "desc": "Should not work",
            "responsible_id": [self.user.id],
            "is_active": True,
        }

        response = self.client.post(self.shops_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_shop_as_superuser(self):
        self.client.force_authenticate(user=self.superuser)

        patch_data = {"desc": "Updated Description"}

        response = self.client.patch(
            self.shop_detail_url, data=patch_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["desc"], "Updated Description")

    def test_patch_shop_as_user_forbidden(self):
        self.client.force_authenticate(user=self.user)

        patch_data = {"desc": "Trying to update"}

        response = self.client.patch(
            self.shop_detail_url, data=patch_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
