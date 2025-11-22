from unittest.mock import patch
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from games.models import Game
from games.serializers import GameSerializer
from json import dumps


class TestGamesView(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()

    @patch('games.views.search_games')
    def test_search_games(self, mock_search_game):
        url = reverse('game-search', kwargs={'search_term': 'mario'})
        mock_search_game.return_value = {"name": "jogo"}

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"name": "jogo"})
        mock_search_game.assert_called_once_with(search_term='mario')

    def test_get_games(self):
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

        url = reverse('game-list-create')
        response = self.client.get(url)

        games = Game.objects.all().order_by('name')
        serializer = GameSerializer(games, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)
