from requests import post
from django.conf import settings


base_url = "https://api.igdb.com/v4"
client_id = settings.IGDB_CLIENT_ID
token = settings.IGDB_TOKEN


def make_request(endpoint, query):
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Content-Type': 'text/plain'
    }

    response = post(
        url=f"{base_url}/{endpoint}",
        headers=headers,
        data=query
    )

    response.raise_for_status()
    return response.json()


def search_games(search_term, limit=10):
    query = f'''
        search "{search_term}";
        fields name, genres.name, age_ratings.rating_category.rating,
        age_ratings.organization.name, summary, release_dates.date, cover.url;
        limit {limit};
    '''

    return make_request(endpoint='games', query=query)


def get_game_by_id(game_id):
    query = f'''
        where id = {game_id};
        fields name, genres.name, age_ratings.rating_category.rating,
        age_ratings.organization.name, summary, release_dates.date, cover.url;
    '''

    return make_request(endpoint='games', query=query)
