import requests
from flask import Flask
import tmdb_client
import random

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OTMyMWNiZmFmM2JkOTUzNmFhNjk2OTJjNjU2NGY3ZSIsInN1YiI6IjY1ZThiOTVmMzQ0YThlMDE0YTNlMjkwYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZURzHk4tXXmZmjHu67aZPFI5lMlx_PdANF_EbmKbjgY"
app = Flask(__name__)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

def get_popular_movies(list_type=None):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_movies(how_many, list_type):
    data = get_popular_movies(list_type)
    return data['results'][:how_many]

def get_random_movies(how_many, list_type):
    data = get_popular_movies(list_type)
    movies = data["results"]
    return random.sample(movies, how_many)

def get_movies_list(list_type):
    endpoint = f"https://api.themoviedb.org/3/movie/{list_type}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    response.raise_for_status()
    return response.json()

def get_single_movie(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_single_movie_cast(movie_id, how_many):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()["cast"][:how_many]

def get_movie_images(movie_id):
    endpoint = f"https://api.themoviedb.org/3/movie/{movie_id}/images"
    headers = {
        "Authorization": f"Bearer {API_TOKEN}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_poster_url(poster_api_path, size = "w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"

def get_backdrop_url(backdrop_api_path, size="w780"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{backdrop_api_path}"

def get_profile_url(profile_api_path, size="w185"):
    if profile_api_path:
        base_url ="https://image.tmdb.org/t/p/"
        return f"{base_url}{size}/{profile_api_path}"
    else:
        return None
    
def get_movie_list():
    return ['popular', 'upcoming', 'top_rated', 'now_playing']