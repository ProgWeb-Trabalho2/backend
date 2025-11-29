from django.urls import path
from .views import UserReviewListCreateView, ReviewUpdateDeleteView, GameReviewListView

urlpatterns = [
    path("user/<int:user_id>/", UserReviewListCreateView.as_view()),
    path("<int:pk>/", ReviewUpdateDeleteView.as_view()),
    path("game/<int:game_id>/", GameReviewListView.as_view()),
]
