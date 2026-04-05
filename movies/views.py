from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone
from core.tmdb_client import TMDBClient
from .serializers import MovieSearchSerializer, TVSearchSerializer, MovieDetailSerializer
from .models import SearchCache
import json


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
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
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