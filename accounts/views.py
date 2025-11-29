from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.parsers import JSONParser

from reviews.models import Review

@permission_classes([AllowAny])
@authentication_classes([])
class RegisterView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        print("DEBUG REGISTER REQUEST.DATA =>", request.data)
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Usuário e senha são obrigatórios"},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Usuário já existe"},
                            status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username,
                                         email=email,
                                         password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email
        }, status=status.HTTP_201_CREATED)


@permission_classes([AllowAny])
@authentication_classes([])
class LoginView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password"),
        )

        if not user:
            return Response({"error": "Credenciais inválidas"},
                            status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email
        })


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = user.profile
        review_count = Review.objects.filter(user=request.user).count()

        return Response({
            "username": user.username,
            "email": user.email,
            "bio": profile.bio,
            "reviews": review_count,
            "avatar": request.build_absolute_uri(profile.avatar.url) if profile.avatar else None
        })

    def patch(self, request):
        user = request.user
        profile = user.profile

        bio = request.data.get("bio")
        avatar = request.FILES.get("avatar")

        if bio is not None:
            profile.bio = bio

        if avatar:
            profile.avatar = avatar

        profile.save()

        return Response({"success": True})


class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            profile = user.profile
        except User.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=404)

        review_count = Review.objects.filter(user=user).count()

        return Response({
            "id": user.id,
            "username": user.username,
            "bio": profile.bio,
            "avatar": request.build_absolute_uri(profile.avatar.url) if profile.avatar else None,
            "reviews": review_count
        })