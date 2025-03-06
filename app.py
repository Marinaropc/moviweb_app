from flask import Flask, jsonify, request, render_template, redirect, url_for
from data_manager.sqlite_data_manager import SQLiteDataManager
from models import db
import config
import requests

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

data_manager = SQLiteDataManager()
OMDB_API_KEY = app.config["OMDB_API_KEY"]

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Welcome to MoviWeb"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route("/add_user", methods = ["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form.get("name")
        if name:
            data_manager.add_user(name)
            return redirect(url_for("list_users"))
    return render_template("add_user.html")


@app.route("/users/<int:user_id>/movies", methods = ["GET"])
def user_movies(user_id):
    user = data_manager.get_user(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    movies = data_manager.get_user_movies(user.id)
    return render_template("users_movies.html",
                           user=user, movies=movies)


@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    if request.method == "POST":
        title = request.form.get("title")
        omdb_url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
        response = requests.get(omdb_url)
        movie_data = response.json()
        if movie_data.get("Response") == "True":
            director = movie_data.get("Director", "Unknown")
            year = movie_data.get("Year", "Unknown")
            rating = movie_data.get("imdbRating", "N/A")
        else:
            director, year, rating = "Unknown", "Unknown", "N/A"
        data_manager.add_movie(user_id, title, director, year, rating)
        return redirect(url_for("user_movies", user_id=user_id))
    return render_template("add_movie.html", user_id=user_id)


@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    movie = data_manager.get_movie(movie_id)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404
    if request.method == "POST":
        name = request.form.get("name")
        director = request.form.get("director")
        year = request.form.get("year")
        rating = request.form.get("rating")
        data_manager.update_movie(movie_id, name, director, year, rating)
        return redirect(url_for("user_movies", user_id=user_id))
    return render_template("update_movie.html",
                           movie=movie, user_id=user_id)


@app.route("/movies/<int:user_id>/delete_movie/<int:movie_id>", methods = ["DELETE"])
def delete_movie(user_id, movie_id):
    movie_to_delete = data_manager.delete_movie(movie_id)
    if movie_to_delete:
        return redirect(url_for("user_movies", user_id = user_id))
    else:
        return jsonify({"message": "Movie not found"}), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Make sure the database and tables are created
    app.run(debug=True)