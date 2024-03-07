import requests
from flask import Flask
import tmdb_client

app = Flask(__name__)

@app.context_processor
def utility_processor():
    def tmdb_image_url(path, size):
        return tmdb_client.get_poster_url(path, size)
    return {"tmdb_image_url": tmdb_image_url}

def get_popular_movies():
    endpoint = "https://api.themoviedb.org/3/movie/popular"
    api_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2OTMyMWNiZmFmM2JkOTUzNmFhNjk2OTJjNjU2NGY3ZSIsInN1YiI6IjY1ZThiOTVmMzQ0YThlMDE0YTNlMjkwYiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.ZURzHk4tXXmZmjHu67aZPFI5lMlx_PdANF_EbmKbjgY"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

def get_poster_url(poster_api_path, size = "w342"):
    base_url = "https://image.tmdb.org/t/p/"
    return f"{base_url}{size}/{poster_api_path}"