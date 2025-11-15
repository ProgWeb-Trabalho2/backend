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

        url = reverse('game-list')
        response = self.client.get(url)

        games = Game.objects.all().order_by('name')
        serializer = GameSerializer(games, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 2)

    def test_post_game_sucesso(self):
        url = reverse('insert-game')

        payload = {
            "name": "last of us",
            "genres": ["action", "adventure"],
            "age_ratings": ["+18"],
            "cover_url": "https://example.com/cover.jpg",
            "release_date": "2013-06-14",
            "summary": "jogo pós apocalíptico de zumbi"
        }

        response = self.client.post(
            url,
            data=dumps(payload),
            content_type="Application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.count(), 1)

        game = Game.objects.first()
        serializer = GameSerializer(game)

        self.assertEqual(response.data, serializer.data)

    def test_post_game_falha(self):
        url = reverse('insert-game')

        payload = {
            "erro": "teste de erro"
        }

        response = self.client.post(
            url,
            data=dumps(payload),
            content_type="Application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_game_sucesso(self):
        game = Game.objects.create(
            id=1,
            name='mario',
            cover_url='url do cover',
            release_date='2013-09-07',
            summary='jogo do encanador italiano'
        )
        url = reverse('delete-game', args=[game.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Game.objects.filter(id=game.id).exists())

    def test_delete_game_falha(self):
        url = reverse('delete-game', args=[3])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Jogo não encontrafo"})
