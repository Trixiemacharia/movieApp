from rest_framework import serializers


class MovieSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField(allow_blank=True)
    release_date = serializers.CharField(allow_blank=True, required=False)
    vote_average = serializers.FloatField()
    popularity = serializers.FloatField()
    poster_path = serializers.SerializerMethodField()
    backdrop_path = serializers.SerializerMethodField()

    def get_poster_path(self, obj):
        path = obj.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500{path}" if path else None

    def get_backdrop_path(self, obj):
        path = obj.get('backdrop_path')
        return f"https://image.tmdb.org/t/p/original{path}" if path else None


class MovieDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    overview = serializers.CharField(allow_blank=True)
    release_date = serializers.CharField(allow_blank=True, required=False)
    vote_average = serializers.FloatField()
    runtime = serializers.IntegerField(required=False)
    genres = serializers.ListField(required=False)
    poster_path = serializers.SerializerMethodField()
    backdrop_path = serializers.SerializerMethodField()

    def get_poster_path(self, obj):
        path = obj.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500{path}" if path else None

    def get_backdrop_path(self, obj):
        path = obj.get('backdrop_path')
        return f"https://image.tmdb.org/t/p/original{path}" if path else None


class TVSearchSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    overview = serializers.CharField(allow_blank=True)
    first_air_date = serializers.CharField(allow_blank=True, required=False)
    vote_average = serializers.FloatField()
    popularity = serializers.FloatField()
    poster_path = serializers.SerializerMethodField()
    backdrop_path = serializers.SerializerMethodField()

    def get_poster_path(self, obj):
        path = obj.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500{path}" if path else None

    def get_backdrop_path(self, obj):
        path = obj.get('backdrop_path')
        return f"https://image.tmdb.org/t/p/original{path}" if path else None