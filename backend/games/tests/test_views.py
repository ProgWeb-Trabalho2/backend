from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from games.models import Game
from games.serializers import GameSerializer


class TestGamesView(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()

        Game.objects.create(
            id=1,
            name='mario',
            cover_url='url do cover',
            release_date='2013-09-07',
            summary='jogo do encanador italiano'
        )
        Game.objects.create(
            id=2,
            name='god of war',
            cover_url='url do cover',
            release_date='2018-02-20',
            summary='mate deuses nórdicos'
        )

    def test_get_games(self):
        url = reverse('game-list')
        response = self.client.get(url)

        games = Game.objects.all().order_by('name')
        serializer = GameSerializer(games, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_post_game(self):
        url = reversed('insert-game')
        response = self.client.post(url)


