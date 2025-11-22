from unittest.mock import patch, Mock
from django.test import TestCase
from django.conf import settings
from games.igdb_service import search_games, make_request, get_game_by_id


class TestIGDBService(TestCase):
    def setUp(self):
        self.search_term = "doom"
        self.game_id = 7351
        self.limit = 10

    @patch('games.igdb_service.post')
    def test_make_request(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = [{"name": "Doom"}]
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        result = make_request("games", "query test")

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

    @patch('games.igdb_service.make_request')
    def test_search_games_build_query(self, mock_make_request):
        search_games("mario", limit=5)

        mock_make_request.assert_called_once()
        kwargs = mock_make_request.call_args.kwargs
        endpoint = kwargs["endpoint"]
        query = kwargs["query"]

        self.assertEqual(endpoint, "games")
        self.assertIn("search \"mario\"", query)
        self.assertIn("limit 5", query)

    @patch('games.igdb_service.make_request')
    def test_get_game_by_id(self, mock_make_request):
        get_game_by_id(self.game_id)

        mock_make_request.assert_called_once()
        kwargs = mock_make_request.call_args.kwargs
        endpoint = kwargs["endpoint"]
        query = kwargs["query"]

        self.assertEqual(endpoint, "games")
        self.assertIn("where id = 7351", query)
