from flask import Flask, render_template, request, url_for, redirect, flash
import random
import tmdb_client
import datetime

app = Flask(__name__)
app.secret_key = b'secret-my'

FAVORITES = set()

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
    movie_list = tmdb_client.get_movie_list()
    selected_list = request.args.get('list_type')
    if selected_list not in movie_list:
        selected_list = 'popular'
    movies = tmdb_client.get_movies(how_many=8, list_type=selected_list)
    return render_template("index.html", movies=movies, current_list=selected_list, movie_list=movie_list)

@app.route("/movie/<movie_id>")
def movie_details(movie_id):
    details = tmdb_client.get_single_movie(movie_id)
    cast = tmdb_client.get_single_movie_cast(movie_id, how_many=8)
    movie_images = tmdb_client.get_movie_images(movie_id)
    selected_backdrop = random.choice(movie_images['backdrops'])
    return render_template("movie_details.html", movie=details, cast=cast, selected_backdrop=selected_backdrop)

@app.route("/search")
def search():
    search_query  = request.args.get("q", "")
    if search_query :
        movies = tmdb_client.search(search_query=search_query)
    else:
        movies = []
    return render_template("search.html", movies=movies, search_query=search_query)

@app.route("/today")
def today():
    movies = tmdb_client.get_airing_today()
    today = datetime.date.today()
    return render_template("today.html", movies=movies, today=today)

@app.route("/favorites/add", methods=['POST'])
def add_to_favorites():
    if request.method == 'POST':
        data = request.form
        movie_id = data.get('movie_id')
        movie_title = data.get('movie_title')
        if movie_id and movie_title:
            FAVORITES.add(movie_id)
            flash(f"Dodano film {movie_title} do ulubionych!")
        return redirect(url_for('homepage'))
    
@app.route("/favorites")
def show_favorite():
    if FAVORITES:
        movies = []
        for movie_id in FAVORITES:
            movie_details = tmdb_client.get_single_movie(movie_id)
            movies.append(movie_details)
    else:
        movies = []
    return render_template("index.html", movies=movies)


if __name__ == "__main__":
    app.run(debug=True)
