from django.urls import path
from reviews.views import CreateReview

urlpatterns = [
    path("", CreateReview.as_view(), name='review-create')
]
