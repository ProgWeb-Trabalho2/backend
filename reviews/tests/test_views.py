from unittest.mock import patch, Mock
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from games.models import Game
from reviews.models import Review
from json import dumps


class TestReviewView(TestCase):
    @classmethod
    def setUpTestData(self):
        self.client = APIClient()

    def setUp(self):
        self.game = Game.objects.create(
            id='1',
            name='mario',
            cover_url='url do cover',
            release_date='2013-09-07',
            summary='jogo do encanador italiano'
        )
        self.user = User.objects.create_user(
            username="jota",
            password="12345678"
        )
        self.token = Token.objects.create(user=self.user)

    def test_create_review_jogo_existe_no_db(self):
        url = reverse('review-create')
        data = {
            "rating": 10,
            "content": "muito bom",
            "user_token": self.token,
            "game_id": 1
        }

        response = self.client.post(
            url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    @patch('reviews.views.get_game_by_id')
    def test_create_review_jogo_nao_existe_no_db(self, mock_get_game_by_id):
        url = reverse('review-create')
        data = {
            "rating": 10,
            "content": "muito bom",
            "user_token": self.token,
            "game_id": 7351
        }

        mock_get_game_by_id.return_value = [
            {
                "id": 7351,
                "age_ratings": [
                    {
                        "id": 69617,
                        "organization": {
                            "id": 3,
                            "name": "CERO"
                        },
                        "rating_category": {
                            "id": 17,
                            "rating": "Z"
                        }
                    },
                    {
                        "id": 79167,
                        "organization": {
                            "id": 6,
                            "name": "CLASS_IND"
                        },
                        "rating_category": {
                            "id": 33,
                            "rating": "18"
                        }
                    },
                    {
                        "id": 79168,
                        "organization": {
                            "id": 7,
                            "name": "ACB"
                        },
                        "rating_category": {
                            "id": 38,
                            "rating": "R 18+"
                        }
                    },
                    {
                        "id": 216192,
                        "organization": {
                            "id": 2,
                            "name": "PEGI"
                        },
                        "rating_category": {
                            "id": 12,
                            "rating": "18"
                        }
                    },
                    {
                        "id": 92322,
                        "organization": {
                            "id": 5,
                            "name": "GRAC"
                        },
                        "rating_category": {
                            "id": 26,
                            "rating": "19+"
                        }
                    },
                    {
                        "id": 79166,
                        "organization": {
                            "id": 4,
                            "name": "USK"
                        },
                        "rating_category": {
                            "id": 22,
                            "rating": "18"
                        }
                    },
                    {
                        "id": 189114,
                        "organization": {
                            "id": 1,
                            "name": "ESRB"
                        },
                        "rating_category": {
                            "id": 6,
                            "rating": "M"
                        }
                    }
                ],
                "cover": {
                    "id": 76903,
                    "url": "//images.igdb.com/igdb/image/upload/t_thumb/co1nc7.jpg"
                },
                "genres": [
                    {
                        "id": 5,
                        "name": "Shooter"
                    },
                    {
                        "id": 9,
                        "name": "Puzzle"
                    }
                ],
                "name": "Doom",
                "release_dates": [
                    {
                        "id": 749942,
                        "date": 1463011200
                    },
                    {
                        "id": 749943,
                        "date": 1463097600
                    },
                    {
                        "id": 749944,
                        "date": 1463097600
                    }
                ],
                "summary": "Developed by id software, the studio that pioneered the first-person shooter genre and created multiplayer Deathmatch, Doom returns as a brutally fun and challenging modern-day shooter experience. Relentless demons, impossibly destructive guns, and fast, fluid movement provide the foundation for intense, first-person combat – whether you’re obliterating demon hordes through the depths of Hell in the single-player campaign, or competing against your friends in numerous multiplayer modes. Expand your gameplay experience using Doom SnapMap game editor to easily create, play, and share your content with the world."
            }
        ]
        response = self.client.post(
            url,
            data=data,
            format="json"
        )
        mock_get_game_by_id.assert_called_once()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(Game.objects.get(id=7351))
        self.assertEqual(Review.objects.count(), 1)

    def test_create_review_erro(self):
        url = reverse('review-create')
        data = {
            "rating": 10,
            "content": 99999,
            "user_token": "não existe",
            "game_id": "não existe"
        }

        response = self.client.post(
            url,
            data=data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
