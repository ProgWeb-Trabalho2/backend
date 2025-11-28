from django.urls import path
from games.views import GameListInsertView, GameDeleteView, GameSearchView, GameSearchByIdView

urlpatterns = [
    path("", GameListInsertView.as_view(), name='game-list-create'),
    path("search/<slug:search_term>",
         GameSearchView.as_view(), name='game-search'),
    path("search-by-id/<int:id>",
         GameSearchByIdView.as_view(), name='game-search-by-id'),
    path("<int:pk>", GameDeleteView.as_view(), name='game-delete')
]
