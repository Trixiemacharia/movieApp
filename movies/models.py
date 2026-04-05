from django.db import models

# Create your models here.
class SearchCache(models.Model):
    cache_key = models.CharField(max_length=255, unique=True)
    result = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'search_cache'

        def __str__(self):
            return self.cache_key