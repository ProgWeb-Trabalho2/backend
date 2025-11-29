from django.db import models


class Game(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    genres = models.JSONField(default=list)
    age_ratings = models.JSONField(default=list)
    summary = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
