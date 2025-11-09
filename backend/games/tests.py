from unittest.mock import patch, Mock
from django.test import TestCase
from django.conf import settings
from games.igdb_service import IGDBService


class TestIGDBService(TestCase):
    def setUp(self):
        self.service = IGDBService()
        self.search_term = "doom"
        self.game_id = 7351
        self.limit = 10

    def test_service_initialization(self):
        assert self.service.client_id == settings.IGDB_CLIENT_ID
        assert self.service.token == settings.IGDB_TOKEN

    @patch('games.igdb_service.post')
    def test_make_request(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = [{"name": "Doom"}]
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = self.service._make_request("games", "query test")

        mock_post.assert_called_once_with(
            url="https://api.igdb.com/v4/games",
            headers={
                'Client-ID': settings.IGDB_CLIENT_ID,
                'Authorization': f'Bearer {settings.IGDB_TOKEN}',
                'Content-Type': 'text/plain'
            },
            data="query test"
        )

        self.assertEqual(result, [{"name": "Doom"}])

    @patch('games.igdb_service.IGDBService._make_request')
    def test_search_games_build_query(self, mock_make_request):
        self.service.search_games("mario", limit=5)

        mock_make_request.assert_called_once()
        kwargs = mock_make_request.call_args.kwargs
        endpoint = kwargs["endpoint"]
        query = kwargs["query"]

        self.assertEqual(endpoint, "games")
        self.assertIn("search mario", query)
        self.assertIn("limit 5", query)
