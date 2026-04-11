import requests
from requests.exceptions import RequestException
from django.conf import settings

class TMDBException(Exception):
    pass

class TMDBRateLimitException(TMDBException):
    pass

class TMDBClient:
    BASE_URL = "http://api.themoviedb.org/3"

    def __init__(self):
        self.api_key = settings.TMDB_API_KEY
        self.session = requests.Session()

    def _get(self, endpoint, params=None):
        """Internal helper method to make all GET requests."""
        if params is None:
            params = {}
        params["api_key"] = self.api_key

        try:
            response = self.session.get(
                f"{self.BASE_URL}{endpoint}",
                params=params,
                timeout=10
            )

            if response.status_code == 429:
                raise Exception(
                    "TMDB rate limit exceeded. Too many requests. Please wait and try again."
                )

            response.raise_for_status()
            return response.json()

        except RequestException as e:
            raise Exception(f"TMDB API request failed: {str(e)}")

    # ── Search ──────────────────────────────────────────
    def search_movies(self, query, page=1):
        """Search for movies by keyword."""
        return self._get("/search/movie", params={"query": query, "page": page})

    def search_tv(self, query, page=1):
        """Search for TV shows by keyword."""
        return self._get("/search/tv", params={"query": query, "page": page})

    # ── Details ─────────────────────────────────────────
    def get_movie_detail(self, movie_id):
        """Get full details for a specific movie."""
        return self._get(f"/movie/{movie_id}")

    def get_tv_detail(self, tv_id):
        """Get full details for a specific TV show."""
        return self._get(f"/tv/{tv_id}")

    # ── Trending ─────────────────────────────────────────
    def get_trending(self, media_type="movie", time_window="day"):
        """
        Get trending movies or TV shows.
        media_type: 'movie' or 'tv'
        time_window: 'day' or 'week'
        """
        return self._get(f"/trending/{media_type}/{time_window}")

    # ── Trailer ──────────────────────────────────────────
    def get_trailer(self, movie_id):
        """Get YouTube trailer for a movie. Returns first trailer found or None."""
        data = self._get(f"/movie/{movie_id}/videos")
        videos = data.get("results", [])

        trailers = [
            v for v in videos
            if v.get("site") == "YouTube" and v.get("type") == "Trailer"
        ]

        if trailers:
            key = trailers[0]["key"]
            return {
                "name": trailers[0]["name"],
                "key": key,
                "url": f"https://www.youtube.com/watch?v={key}"
            }
        return None
