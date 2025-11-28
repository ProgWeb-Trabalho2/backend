from django.urls import path
from games.views import GameListInsertView, GameDeleteView

urlpatterns = [
    path("", GameListInsertView.as_view(), name='game-list-create'),
    path("<int:pk>", GameDeleteView.as_view(), name='game-delete')
]
