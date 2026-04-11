from rest_framework import serializers
from .models import Favourite


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = [
            'id', 'media_id', 'media_type', 'title',
            'poster_path', 'vote_average', 'added_at'
        ]
        read_only_fields = ['id', 'added_at']

    def create(self, validated_data):
        user = self.context['request'].user
        # Prevent duplicates
        favourite, created = Favourite.objects.get_or_create(
            user=user,
            media_id=validated_data['media_id'],
            media_type=validated_data['media_type'],
            defaults={
                'title': validated_data['title'],
                'poster_path': validated_data.get('poster_path'),
                'vote_average': validated_data.get('vote_average', 0.0),
            }
        )
        if not created:
            raise serializers.ValidationError(
                {"detail": "This item is already in your favourites."}
            )
        return favourite