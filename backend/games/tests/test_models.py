from django.test import TestCase
from games.models import Game


class TestGameModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        Game.objects.create(
            id=1,
            name='mario',
            cover_url='url do cover',
            release_date='2013-09-07',
            summary='jogo do encanador italiano'
        )

    def test_model_return_name(self):
        game = Game.objects.get(id=1)
        expected_name = f'{game.name}'

        self.assertEqual(str(game), expected_name)
