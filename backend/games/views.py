from games.serializers import GameSerializer
from games.models import Game
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class GamesView(APIView):
    def get(self, request):
        queryset = Game.objects.all().order_by('name')
        serializer = GameSerializer(queryset, many=True)
        return Response(serializer.data)

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

    def delete(self, request, pk):
        try:
            game = Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            return Response(
                {"error": "Jogo não encontrafo"},
                status=status.HTTP_404_NOT_FOUND
            )

        game.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
