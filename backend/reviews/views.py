from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from games.models import Game
from games.serializers import GameSerializer
from games.igdb_service import get_game_by_id
from reviews.serializer import ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from datetime import datetime


class CreateReview(APIView):
    @swagger_auto_schema(
        request_body=ReviewSerializer,
        responses={
            201: ReviewSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                )
            )
        }
    )
    def post(self, request):
        user_id = None
        game_id = None

        try:
            user_id = Token.objects.get(
                key=request.data.get("user_token")).user.id
        except Token.DoesNotExist:
            return Response(
                {"error": "Usuário não existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            game = Game.objects.get(id=request.data.get("game_id"))
            game_id = game.id
        except Game.DoesNotExist:
            game = get_game_by_id(request.data.get("game_id"))
            if not game:
                return Response(
                    {"error": "Jogo não existe"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            game = game[0]
            game_id = game['id']
            new_game = GameSerializer(data={
                "id": game_id,
                "name": game["name"],
                "genres": game["genres"],
                "age_ratings": game["age_ratings"],
                "summary": game["summary"],
                "release_date": datetime.fromtimestamp(game["release_dates"][0]["date"]).date(),
                "cover_url": "https:" + game["cover"]["url"]
            })

            if not new_game.is_valid():
                return Response(
                    new_game.errors,
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            new_game.save()

        data = {
            "rating": int(request.data.get("rating")),
            "content": request.data.get("content"),
            "user": user_id,
            "game": game_id
        }

        serializer = ReviewSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )
