from django.contrib.auth.models import User
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from games.models import Game
from reviews.serializer import ReviewSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


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
        serializer = ReviewSerializer(data=request.data)
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
