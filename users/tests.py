from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()


class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "strongpass123",
            "first_name": "Иван",
            "last_name": "Иванов",
            "age": 25,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_jwt_token_obtain(self):
        User.objects.create_user(username="testuser", password="testpass123")
        url = reverse("token_obtain_pair")
        response = self.client.post(
            url, {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_users_list_requires_auth(self):
        url = reverse("user_list")
        response = self.client.get(url)
        self.assertIn(response.status_code, [401, 403])

    def test_users_list_accessible_when_logged_in(self):
        User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        url = reverse("user_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
