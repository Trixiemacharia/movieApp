from django.db import models
from django.conf import settings


class Favourite(models.Model):
    MEDIA_TYPES = [
        ('movie', 'Movie'),
        ('tv', 'TV Show'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favourites'
    )
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    title = models.CharField(max_length=255)
    poster_path = models.URLField(blank=True, null=True)
    vote_average = models.FloatField(default=0.0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'favourites'
        unique_together = ('user', 'media_id', 'media_type')

    def __str__(self):
        return f"{self.user.email} - {self.title}"