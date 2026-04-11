from django.db import models
from django.conf import settings

# Create your models here.
class SearchCache(models.Model):
    cache_key = models.CharField(max_length=255, unique=True)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'search_cache'

        def __str__(self):
            return self.cache_key
        
class WatchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watch_history'
    )
    media_id = models.IntegerField()
    media_type = models.CharField(max_length=10, default='movie')
    title = models.CharField(max_length=255)
    poster_path = models.URLField(blank=True, null=True)
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'watch_history'
        ordering = ['-watched_at']

        def __str__(self):
            return f"{self.user.email} - {self.title}"