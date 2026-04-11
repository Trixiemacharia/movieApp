from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from core.tmdb_client import TMDBClient,TMDBRateLimitException
from .serializers import MovieSearchSerializer, TVSearchSerializer, MovieDetailSerializer
from .models import SearchCache, WatchHistory
import json

def handle_tmdb_error(e):
    if isinstance(e, TMDBRateLimitException):
        response = Response(
            {"error": "TMDB rate limit exceeded. Please try again later."},
            status= status.HTTP_503_SERVICE_UNAVAILABLE
        )
        response["Retry-After"] = str(e)
        return response
    return Response(
        {"error": str(e)},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

# ── Movie Search ─────────────────────────────────────────
class MovieSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        page = request.query_params.get('page', 1)

        if not query:
            return Response(
                {"error": "Query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check cache first
        cache_key = f"movie_search_{query}_page_{page}"
        cached = SearchCache.objects.filter(cache_key=cache_key).first()
        if cached:
            print(f"CACHE HIT: {cache_key}")
            return Response({**json.loads(cached.result), "cached": True})

        try:
            client = TMDBClient()
            data = client.search_movies(query, page=int(page))
            serializer = MovieSearchSerializer(data['results'], many=True)

            result = {
                "page": data.get("page", 1),
                "total_pages": data.get("total_pages", 1),
                "total_results": data.get("total_results", 0),
                "results": serializer.data
            }

            # Save to cache
            SearchCache.objects.create(
                cache_key=cache_key,
                result=json.dumps(result)
            )

            return Response({**result, "cached": False})

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ── Movie Detail ─────────────────────────────────────────
class MovieDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        try:
            client = TMDBClient()
            data = client.get_movie_detail(movie_id)
            serializer = MovieDetailSerializer(data)

            WatchHistory.objects.get_or_create(
                user = request.user,
                media_id = movie_id,
                media_type='movie',
                defaults={
                    'title': data.get('title',''),
                    'poster_path':f"https://image.tmdb.org/t/p/w500{data.get('poster_path')}"
                    if data.get('poster_path') else None,
                }
            )
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ── Trending View ─────────────────────────────────────────
class TrendingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        media_type = request.query_params.get('type', 'movie')
        time_window = request.query_params.get('window', 'day')

        # Validate params
        if media_type not in ['movie', 'tv']:
            return Response(
                {"error": "type must be 'movie' or 'tv'"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if time_window not in ['day', 'week']:
            return Response(
                {"error": "window must be 'day' or 'week'"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            client = TMDBClient()
            data = client.get_trending(
                media_type=media_type,
                time_window=time_window
            )

            if media_type == 'movie':
                serializer = MovieSearchSerializer(data['results'], many=True)
            else:
                serializer = TVSearchSerializer(data['results'], many=True)

            return Response({
                "media_type": media_type,
                "time_window": time_window,
                "total_results": len(data['results']),
                "results": serializer.data
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ── Watch History View ────────────────────────────────────
class WatchHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        history = WatchHistory.objects.filter(
            user=request.user
        ).order_by('-watched_at')

        data = [{
            "id": h.id,
            "media_id": h.media_id,
            "media_type": h.media_type,
            "title": h.title,
            "poster_path": h.poster_path,
            "watched_at": h.watched_at,
        } for h in history]

        return Response({"results": data})

    def delete(self, request):
        WatchHistory.objects.filter(user=request.user).delete()
        return Response(
            {"message": "Watch history cleared."},
            status=status.HTTP_200_OK
        )
    
# ── Trailer View ──────────────────────────────────────────
class TrailerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        try:
            client = TMDBClient()
            trailer = client.get_trailer(movie_id)

            if not trailer:
                return Response(
                    {"error": "No trailer found for this movie."},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response({
                "movie_id": movie_id,
                "trailer": trailer
            })

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ── TV Search ─────────────────────────────────────────────
class TVSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '').strip()
        page = request.query_params.get('page', 1)

        if not query:
            return Response(
                {"error": "Query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check cache first
        cache_key = f"tv_search_{query}_page_{page}"
        cached = SearchCache.objects.filter(cache_key=cache_key).first()
        if cached:
            print(f"CACHE HIT: {cache_key}")
            return Response({**json.loads(cached.result), "cached": True})

        try:
            client = TMDBClient()
            data = client.search_tv(query, page=int(page))
            serializer = TVSearchSerializer(data['results'], many=True)

            result = {
                "page": data.get("page", 1),
                "total_pages": data.get("total_pages", 1),
                "total_results": data.get("total_results", 0),
                "results": serializer.data
            }

            # Save to cache
            SearchCache.objects.create(
                cache_key=cache_key,
                result=json.dumps(result)
            )

            return Response({**result, "cached": False})

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ── TV Detail ─────────────────────────────────────────────
class TVDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, tv_id):
        try:
            client = TMDBClient()
            data = client.get_tv_detail(tv_id)
            return Response(data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )