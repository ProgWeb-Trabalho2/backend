from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient


class TestCreateAccount(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_create_user_sucesso(self):
        user = {
            "username": "jota",
            "password": "babaca12"
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_create_user_usuario_ja_existe(self):
        User.objects.create_user(
            username="jota",
            password="12345678"
        )
        user = {
            "username": "jota",
            "password": "babaca12"
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_senha_invalida(self):
        user = {
            "username": "jota",
            "password": "banana"
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
