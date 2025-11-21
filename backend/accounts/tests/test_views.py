from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class TestLogin(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()
        self.url = reverse('login')

    def setUp(self):
        user = User.objects.create_user(username="jota", password="babaca12")
        Token.objects.create(user=user)

    def test_sucesso(self):
        user = {
            "username": "jota",
            "password": "babaca12"
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_username_senha_inexistentes(self):
        user = {
            "username": "",
            "password": ""
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"error": "Usuário e senha obrigatórios"})

    def test_user_nao_existe(self):
        user = {
            "username": "inexistente",
            "password": "aaaaaaaaaa"
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Usuário não existe"})


class TestCreateAccount(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()
        self.url = reverse('register')

    def test_sucesso(self):
        user = {
            "username": "jota",
            "password": "babaca12"
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue('token' in response.data)

    def test_usuario_ja_existe(self):
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
        self.assertEqual(response.data, {"error": "Usuário já existe"})

    def test_senha_invalida(self):
        user = {
            "username": "jota",
            "password": "banana"
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('error' in response.data)

    def test_username_senha_inexistentes(self):
        user = {
            "username": "",
            "password": ""
        }

        response = self.client.post(self.url, data=user)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"error": "Usuário e senha obrigatórios"})
