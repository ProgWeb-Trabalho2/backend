from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginView(ObtainAuthToken):
    @swagger_auto_schema(
        operation_summary='Realiza login',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        ),
        responses={
            status.HTTP_200_OK: 'token',
            status.HTTP_400_BAD_REQUEST: 'Bad request',
        },
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Usuário e senha obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not User.objects.filter(username=username).exists():
            return Response(
                {"error": "Usuário não existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.get(username=username)

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token = Token.objects.get(user=user)

        return Response(
            {
                'token': token.key,
                'username': user.username
            },
            status=status.HTTP_200_OK
        )


class RegisterView(ObtainAuthToken):
    @swagger_auto_schema(
        operation_summary='Realiza cadastro',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['username', 'password']
        ),
        responses={
            status.HTTP_200_OK: 'token',
            status.HTTP_400_BAD_REQUEST: 'Bad request',
        },
    )
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Usuário e senha obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Usuário já existe"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password=password)
        except ValidationError as e:
            return Response(
                {"error": e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(username=username, password=password)

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'token': token.key,
                'username': user.username
            },
            status=status.HTTP_201_CREATED
        )
