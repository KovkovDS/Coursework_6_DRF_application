from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from users.models import User


class TestCase(APITestCase):
    """Базовый тестовый класс для всех тестов."""

    def setUp(self):
        """Задает начальные данные для тестов."""

        self.user = User.objects.create(email="test_admin@sky.pro")
        self.user.is_active = True
        self.user.is_superuser = True
        self.client.force_authenticate(user=self.user)


class ProfileTestCase(TestCase, APITestCase):
    """Тесты для работы с пользователями."""

    def test_list_profiles(self):
        """Тест на получение списка пользователей."""

        url = reverse("users:profiles")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = [
            {
                "avatar": self.user.avatar,
                "city": self.user.city,
                "email": self.user.email,
            }
        ]
        self.assertEqual(data, result)

    def test_retrieve_profile(self):
        """Тест получения пользователя по Primary Key."""

        url = reverse("users:profile", args=(self.user.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], self.user.email)

    def test_create_profile(self):
        """Тест создания нового пользователя."""

        url = reverse("users:registration")
        data = {"email": "test_user__for_test@sky.pro", "password": "test_user12345"}
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email="test_user__for_test@sky.pro").count(), 1)
        self.assertTrue(User.objects.all().exists())

    def test_update_profile(self):
        """Тест изменения пользователя по Primary Key."""

        url = reverse("users:update_profile", args=(self.user.pk,))
        data = {
            "email": "updated_test_user__for_test@sky.pro",
            "password": "test_user123456",
            "phone_number": "79865432112",
            "city": "Volgograd",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(pk=self.user.pk).city, "Volgograd")

    def test_delete_profile(self):
        """Тест удаления пользователя по Primary Key."""

        url = reverse("users:delete_profile", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
