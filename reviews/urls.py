from django.urls import path
from .views import UserReviewListCreateView, ReviewUpdateDeleteView

urlpatterns = [
    path("user/<int:user_id>/", UserReviewListCreateView.as_view()),
    path("<int:pk>/", ReviewUpdateDeleteView.as_view()),
]
