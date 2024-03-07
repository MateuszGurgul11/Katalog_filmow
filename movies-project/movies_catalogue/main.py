from flask import Flask, render_template
import tmdb_client

app = Flask(__name__)

@app.context_processor
def utility_processor():
    def tmdb_image_url(poster_path, size="w342"):
        return tmdb_client.get_poster_url(poster_path, size)
    return {"tmdb_image_url": tmdb_image_url}

@app.route("/")
def homepage():
    # Pobieranie listy filmów i przekazanie ich do szablonu
    movies = tmdb_client.get_popular_movies()["results"][:8]
    return render_template("index.html", movies=movies)

if __name__ == "__main__":
    app.run(debug=True)
