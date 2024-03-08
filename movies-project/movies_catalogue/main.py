from flask import Flask, render_template
import tmdb_client

app = Flask(__name__)

@app.context_processor
def utility_processor():
    def tmdb_image_url(poster_path=None, backdrop_path=None, profile_path=None, size_p="w342", size_b="w780"):
        if backdrop_path:
            return tmdb_client.get_backdrop_url(backdrop_path, size_p)
        elif poster_path:
            return tmdb_client.get_poster_url(poster_path, size_b)
        elif profile_path:
            return tmdb_client.get_profile_url(profile_path)
        else:
            return None
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/")
def homepage():
    movies = tmdb_client.get_random_movies(how_many=8)
    return render_template("index.html", movies=movies)

@app.route('/movie/<movie_id>')
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id)
    return render_template("movie_details.html", movie=details, cast=cast)

if __name__ == "__main__":
    app.run(debug=True)
