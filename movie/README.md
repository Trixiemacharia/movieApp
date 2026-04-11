# 🎬 MovieApp API

A Django REST Framework backend that integrates with TMDB API.

## 🚀 Setup

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🔐 Authentication
All endpoints (except register/login) require JWT token:
## 📌 Endpoints

### Auth
| Method | URL | Description |
|--------|-----|-------------|
| POST | `/api/users/register/` | Register new user |
| POST | `/api/users/login/` | Login and get JWT tokens |
| GET | `/api/users/profile/` | Get user profile |
| PATCH | `/api/users/profile/` | Update profile |
| POST | `/api/users/token/refresh/` | Refresh access token |

### Movies
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/movies/search/?q=<query>` | Search movies |
| GET | `/api/movies/<id>/` | Movie detail |
| GET | `/api/movies/<id>/trailer/` | Get trailer |
| GET | `/api/movies/trending/` | Trending movies |
| GET | `/api/movies/trending/?type=tv&window=week` | Trending TV shows |
| GET | `/api/movies/tv/search/?q=<query>` | Search TV shows |
| GET | `/api/movies/tv/<id>/` | TV show detail |

### Favourites
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/favourites/` | List favourites |
| POST | `/api/favourites/` | Add favourite |
| DELETE | `/api/favourites/<id>/` | Remove favourite |

### Watch History
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/movies/history/` | Get watch history |
| DELETE | `/api/movies/history/` | Clear watch history |

### Health
| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/health/` | Health check |

## 📦 Request/Response Examples

### Register
**Request:**
```json
{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}
```
**Response:**
```json
{
    "message": "User registered successfully.",
    "user": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }
}
```

### Movie Search
**Response:**
```json
{
    "page": 1,
    "total_pages": 10,
    "total_results": 100,
    "cached": false,
    "results": [
        {
            "id": 27205,
            "title": "Inception",
            "overview": "A thief...",
            "release_date": "2010-07-15",
            "vote_average": 8.4,
            "poster_path": "https://image.tmdb.org/t/p/w500/...",
            "backdrop_path": "https://image.tmdb.org/t/p/original/..."
        }
    ]
}
```

### Add Favourite
**Request:**
```json
{
    "media_id": 27205,
    "media_type": "movie",
    "title": "Inception",
    "vote_average": 8.4
}
```
**Response:**
```json
{
    "id": 1,
    "media_id": 27205,
    "media_type": "movie",
    "title": "Inception",
    "vote_average": 8.4,
    "added_at": "2026-04-05T12:00:00Z"
}
```