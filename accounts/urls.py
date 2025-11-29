from django.urls import path
from .views import RegisterView, LoginView, MeView, PublicProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("me/", MeView.as_view()),
    path("user/<int:user_id>/", PublicProfileView.as_view()),
]