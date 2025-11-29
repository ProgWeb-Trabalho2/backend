from django.test import TestCase
from django.contrib.auth.models import User
from games.models import Game
from reviews.models import Review


class TestReview(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='teste', password='password123'
        )
        cls.game = Game.objects.create(
            id=1,
            name='mario',
            cover_url='url do cover',
            release_date='2013-09-07',
            summary='jogo do encanador italiano'
        )
        Review.objects.create(
            user=cls.user,
            game=cls.game,
            rating=10,
            content='jogo muito massa',
        )

    def test_model_return_name(self):
        review = Review.objects.get(id=1)
        expected_name = f"Avaliação de {review.user.username} para {
            review.game.name}: nota {review.rating}"

        self.assertEqual(str(review), expected_name)
