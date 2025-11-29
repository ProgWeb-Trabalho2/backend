from django.urls import path
from .views import GameSearchView, GameSearchByIdView

urlpatterns = [
    path("search/<slug:search_term>/", GameSearchView.as_view()),
    path("search-by-id/<int:id>/", GameSearchByIdView.as_view()),
]
