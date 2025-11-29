from rest_framework import serializers
from .models import Review
from django.contrib.auth.models import User
from games.models import Game

class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    user_avatar = serializers.SerializerMethodField()
    game = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id",
            "user_username",
            "user_avatar",
            "user_id",
            "game",
            "game_id",
            "score",
            "comment",
            "created_at"
        ]

    def get_user_avatar(self, obj):
        profile = getattr(obj.user, "profile", None)
        if profile and profile.avatar:
            request = self.context.get("request")
            return request.build_absolute_uri(profile.avatar.url)
        return None

    def get_game(self, obj):
        try:
            game = Game.objects.get(id=obj.game_id)
            request = self.context.get("request")
            return {
                "name": game.name,
                "cover": request.build_absolute_uri(game.cover.url) if game.cover else None,
            }
        except Game.DoesNotExist:
            return {
                "name": "Jogo desconhecido",
                "cover": None
            }
