from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from games.models import Game
from json import dumps


class TestReviewView(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()

    def setUp(self):
        self.game = Game.objects.create(
            name='mario',
            cover_url='url do cover',
            release_date='2013-09-07',
            summary='jogo do encanador italiano'
        )
        self.user = User.objects.create_user(
            username="jota",
            password="12345678"
        )

    def test_create_review_sucesso(self):
        url = reverse('review-create')
        data = {
            "rating": 10,
            "content": "muito bom",
            "user": self.user.id,
            "game": self.game.id
        }

        response = self.client.post(
            url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_erro(self):
        url = reverse('review-create')
        data = {
            "rating": 10,
            "content": 99999,
            "user": "não existe",
            "game": "não existe"
        }

        response = self.client.post(
            url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
