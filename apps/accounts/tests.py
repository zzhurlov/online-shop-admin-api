from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.hashers import make_password

from apps.accounts.models import User
from apps.accounts.serializers import (
    CreateUserSerializer,
    ProfileSerializer,
    ResponsibleSerializer,
)

from django.test import TestCase
from django.urls import reverse


# Models testing
class UserModelTest(TestCase):
    def setUp(self):
        self.responsible = User.objects.create_responsible(
            first_name="Aleksey",
            last_name="Voronov",
            email="voronov@ya.ru",
            password="admin",
        )

    def test_responisble_creation(self):
        self.assertEqual(self.responsible.first_name, "Aleksey")
        self.assertEqual(self.responsible.last_name, "Voronov")
        self.assertEqual(self.responsible.email, "voronov@ya.ru")

    def test_user_str_method(self):
        self.assertEqual(str(self.responsible), "Aleksey Voronov")


# Endpoints testing
class RegisterAccountAPITestCase(APITestCase):
    """Testing endpoints of accounts application"""

    def setUp(self):
        self.superuser = User.objects.create_superuser(
            first_name="testsuperuser",
            last_name="test",
            email="test@test.ru",
            password="test",
            role="SUPERUSER",
        )
        self.client.login(email="test@test.ru", password="test")
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_register_user(self):
        data = {
            "first_name": "test",
            "last_name": "test",
            "email": "test@ya.ru",
            "password": "test",
        }

        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ProfileAPITestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            first_name="testsuperuser",
            last_name="test",
            email="test@test.ru",
            password="test",
            role="SUPERUSER",
        )
        self.client.login(email="test@test.ru", password="test")
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_get_profile_by_email(self):
        response = self.client.get(
            reverse("profile", kwargs={"email": self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_profile_by_email(self):
        data = {
            "first_name": "Test",
            "last_name": "Testov",
            "email": "user@example.com",
            "is_active": True,
            "is_staff": True,
            "role": "RESP",
        }
        response = self.client.patch(
            reverse("profile", kwargs={"email": self.user.email}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_profile_by_email(self):
        response = self.client.delete(
            reverse("profile", kwargs={"email": self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProfilesAPITestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            first_name="testsuperuser",
            last_name="test",
            email="test@test.ru",
            password="test",
            role="SUPERUSER",
        )
        self.client.login(email="test@test.ru", password="test")

    def test_get_all_profiles(self):
        response = self.client.get(reverse("profiles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class MyProfileAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )
        self.client.login(email="email@email.ru", password="test")

    def test_get_my_profile(self):
        response = self.client.get(reverse("myprofile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_my_profile(self):
        data = {
            "first_name": "Test",
            "last_name": "Testov",
            "email": "user@example.com",
            "is_active": True,
            "is_staff": True,
            "role": "RESP",
        }
        response = self.client.patch(reverse("myprofile"), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Permissions testing
class RegisterAccountPermissionTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            first_name="testsuperuser",
            last_name="test",
            email="test@test.ru",
            password="test",
            role="SUPERUSER",
        )
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_admin_can_register_user(self):
        self.client.login(email="test@test.ru", password="test")

        data = {
            "first_name": "test",
            "last_name": "testov",
            "email": "test@ya.ru",
            "password": "test",
        }

        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_register_another_user(self):
        self.client.login(email="email@email.ru", password="test")

        data = {
            "first_name": "test",
            "last_name": "testov",
            "email": "test@ya.ru",
            "password": "test",
        }

        response = self.client.post(reverse("signup"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RUDProfilePermissionTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            first_name="testsuperuser",
            last_name="test",
            email="test@test.ru",
            password="test",
            role="SUPERUSER",
        )
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_admin_can_get_user_profile(self):
        self.client.login(email="test@test.ru", password="test")

        response = self.client.get(
            reverse("profile", kwargs={"email": self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_get_user_profile(self):
        self.client.login(email="email@email.ru", password="test")

        response = self.client.get(
            reverse("profile", kwargs={"email": self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_patch_user_profile(self):
        self.client.login(email="test@test.ru", password="test")

        data = {
            "first_name": "Test",
            "last_name": "Testov",
            "email": "user@example.com",
            "is_active": True,
            "is_staff": True,
            "role": "RESP",
        }
        response = self.client.patch(
            reverse("profile", kwargs={"email": self.user.email}),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_patch_user_profile(self):
        self.client.login(email="email@email.ru", password="test")

        data = {
            "first_name": "Test",
            "last_name": "Testov",
            "email": "user@example.com",
            "is_active": True,
            "is_staff": True,
            "role": "RESP",
        }
        response = self.client.patch(
            reverse("profile", kwargs={"email": self.user.email}),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_user_profile(self):
        self.client.login(email="test@test.ru", password="test")

        response = self.client.delete(
            reverse("profile", kwargs={"email": self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_user_profile(self):
        self.client.login(email="email@email.ru", password="test")

        response = self.client.delete(
            reverse("profile", kwargs={"email": self.user.email})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ProfilesPermissionTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            first_name="testsuperuser",
            last_name="test",
            email="test@test.ru",
            password="test",
            role="SUPERUSER",
        )
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_admin_can_get_all_profiles(self):
        self.client.login(email="test@test.ru", password="test")

        response = self.client.get(reverse("profiles"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_get_all_profiles(self):
        self.client.login(email="email@email.ru", password="test")

        response = self.client.get(reverse("profiles"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MyProfilePermissionTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            first_name="testsuperuser",
            last_name="test",
            email="test@test.ru",
            password="test",
            role="SUPERUSER",
        )
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_anon_cannot_get_his_profile(self):
        response = self.client.get(reverse("myprofile"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_get_his_profile(self):
        self.client.login(email="email@email.ru", password="test")

        response = self.client.get(reverse("myprofile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_get_his_profile(self):
        self.client.login(email="test@test.ru", password="test")

        response = self.client.get(reverse("myprofile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Serializers testing
class CreateUserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_user_serialization(self):
        serializer = CreateUserSerializer(self.user)
        data = serializer.data
        data.pop("password")
        expected_data = {
            "first_name": "test_user",
            "last_name": "test",
            "email": "email@email.ru",
        }
        self.assertEqual(data, expected_data)

    def test_user_validation(self):
        invalid_data = {
            "first_name": "abcdeabcdeabcdeabcdeabcdeabcdee",
            "last_name": "abcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcde",
            "email": "email",
        }
        serializer = CreateUserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn("last_name", serializer.errors)
        self.assertIn("email", serializer.errors)


class ProfileSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_profile_serialization(self):
        serializer = ProfileSerializer(self.user)
        expected_data = {
            "id": self.user.id,
            "last_login": None,
            "first_name": "test_user",
            "last_name": "test",
            "email": "email@email.ru",
            "is_active": True,
            "is_staff": True,
            "role": "RESP",
            "avatar": "/media/avatars/default.jpg",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_profile_validation(self):
        invalid_data = {
            "last_login": 4,
            "first_name": "abcdeabcdeabcdeabcdeabcdeabcdee",
            "last_name": "abcdeabcdeabcdeabcdeabcdeabcdeabcdeabcdeabcde",
            "email": "email",
            "avatar": 0,
        }
        serializer = ProfileSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class ResponsibleSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_responsible(
            first_name="test_user",
            last_name="test",
            email="email@email.ru",
            password="test",
        )

    def test_responsible_serialization(self):
        serializer = ResponsibleSerializer(self.user)
        expected_data = {
            "id": self.user.id,
            "first_name": "test_user",
            "last_name": "test",
            "email": "email@email.ru",
            "is_active": True,
            "role": "RESP",
        }
        self.assertEqual(serializer.data, expected_data)

    def test_responsible_validation(self):
        invalid_data = {
            "id": self.user.id,
            "last_login": 43,
            "first_name": "andfbsdfcnscdfggcdfgcgcdfcgdgdg",
            "last_name": "andfbsdfcnscdfggcdfgcgcdfcgdgdgrtete",
            "email": "email@emru",
            "is_active": 324,
            "is_staff": "-",
            "role": "REdfsg",
            "avatar": 0,
        }
        serializer = ResponsibleSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
