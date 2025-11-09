from requests import post
from django.conf import settings


class IGDBService:
    def __init__(self):
        self.base_url = "https://api.igdb.com/v4"
        self.client_id = settings.IGDB_CLIENT_ID
        self.token = settings.IGDB_TOKEN

    def _make_request(self, endpoint, query):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'text/plain'
        }

        response = post(
            url=f"{self.base_url}/{endpoint}",
            headers=headers,
            data=query
        )

        response.raise_for_status()
        return response.json()

    def search_games(self, search_term, limit=10):
        query = f'''
            search {search_term};
            fields name, genres.name, age_ratings.rating_category.rating,
            age_ratings.organization.name, summary, release_date.date, cover.url;
            limit {limit};
        '''

        return self._make_request(endpoint='games', query=query)
