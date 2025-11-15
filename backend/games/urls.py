from django.urls import path
from games.views import GamesView

urlpatterns = [
    path("lista/", GamesView.as_view(), name='game-list'),
    path("insert/", GamesView.as_view(), name='insert-game'),
    path("delete/<int:pk>", GamesView.as_view(), name='delete-game')
]
