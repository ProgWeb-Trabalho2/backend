from django.db import models
from django.contrib.auth.models import User
from games.models import Game


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Avaliação de {self.user.username} para {self.game.name}: nota {self.rating}"

    class Meta:
        unique = ['user', 'game']
