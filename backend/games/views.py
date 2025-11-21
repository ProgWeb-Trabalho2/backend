from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from games.serializers import GameSerializer
from games.models import Game
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class GameListInsertView(APIView):
    @swagger_auto_schema(
        request_body=None,
        responses={
            200: GameSerializer(many=True)
        }
    )
    def get(self, request):
        queryset = Game.objects.all().order_by('name')
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=GameSerializer,
        responses={
            201: GameSerializer,
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING)
                ),
                description="Erros de validação"
            )
        }
    )
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class GameDeleteView(APIView):
    @swagger_auto_schema(
        responses={
            204: "Jogo deletado com sucesso",
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Jogo não encontrado"
                    )
                }
            )
        }
    )
    def delete(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(
                {"error": "Jogo não encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        game.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
