from flask import (Flask, jsonify, request, render_template,
                   redirect, url_for, flash)
from data_manager.sqlite_data_manager import SQLiteDataManager
from models import db
from sqlalchemy.exc import SQLAlchemyError
from jinja2 import TemplateNotFound, TemplateSyntaxError
import config
import requests

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)

data_manager = SQLiteDataManager()
OMDB_API_KEY = app.config["OMDB_API_KEY"]

with app.app_context():
    db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route("/")
def home():
    return render_template("home.html")


@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()
        if not users:
            flash("No users found")
            return render_template('users.html, users=[]')
        return render_template('users.html', users=users)
    except SQLAlchemyError as e:
        print("database error", e)
        return render_template('500.html'), 500
    except TemplateNotFound as e:
        print("template not found", e), 500
    except TemplateSyntaxError as e:
        print("template syntax error", e),500


@app.route("/add_user", methods = ["GET", "POST"])
def add_user():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            if not name:
                flash("Please enter a name")
                return render_template("add_user.html")
            user_added =data_manager.add_user(name)
            if user_added:
                flash("User added successfully!", "success")
            else:
                flash("An error occurred", "error")
            return redirect(url_for("list_users"))
        return render_template("add_user.html")
    except SQLAlchemyError as e:
        print("database error", e)
        return render_template('500.html'), 500


@app.route("/users/<int:user_id>/movies", methods = ["GET"])
def user_movies(user_id):
    try:
        user = data_manager.get_user(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        movies = data_manager.get_user_movies(user.id)
        return render_template("users_movies.html",
                               user=user, movies=movies)
    except SQLAlchemyError as e:
        print("database error", e)
        return render_template('500.html'), 500
    except TemplateNotFound as e:
        print("template not found", e), 500
    except TemplateSyntaxError as e:
        print("template syntax error", e),500


@app.route("/users/<int:user_id>/add_movie", methods=["GET", "POST"])
def add_movie(user_id):
    try:
        if request.method == "POST":
            title = request.form.get("title")
            if not title:
                flash("Movie title is required.", "error")
                return redirect(url_for("add_movie", user_id=user_id))
            omdb_url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"

            try:
                response = requests.get(omdb_url, timeout=5)
                response.raise_for_status()
                movie_data = response.json()
            except requests.RequestException as e:
                flash("Failed to retrieve movie data. Please try again later.", "error")
                print("OMDb API request error:", e)
                return redirect(url_for("add_movie", user_id=user_id))

            if movie_data.get("Response") == "True":
                director = movie_data.get("Director", "Unknown")
                year = movie_data.get("Year", "Unknown")
                rating = movie_data.get("imdbRating", "N/A")
                poster = movie_data.get("Poster", "https://via.placeholder.com/150")
            else:
                flash("Movie not found in OMDb.", "error")
                return redirect(url_for("add_movie", user_id=user_id))

            try:
                data_manager.add_movie(user_id, title, director, year, rating, poster)
            except SQLAlchemyError as e:
                flash("Database error while adding movie.", "error")
                print("Database error:", e)
                return render_template('500.html'), 500

            flash("Movie added successfully!", "success")
            return redirect(url_for("user_movies", user_id=user_id))

        return render_template("add_movie.html", user_id=user_id)

    except Exception as e:
        flash("An unexpected error occurred.", "error")
        print("Unexpected error:", e)
        return render_template("500.html"), 500


@app.route("/users/<int:user_id>/update_movie/<int:movie_id>", methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    try:
        movie = data_manager.get_movie(movie_id)
        if not movie:
            flash("Movie not found.", "error")
            return jsonify({"message": "Movie not found"}), 404

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            director = request.form.get("director", "").strip()
            year = request.form.get("year", "").strip()
            rating = request.form.get("rating", "").strip()

            if not name or not director or not year or not rating:
                flash("All fields are required.", "error")
                return render_template("update_movie.html", movie=movie, user_id=user_id)
            try:
                data_manager.update_movie(movie_id, name, director, year, rating)
                flash("Movie updated successfully!", "success")
                return redirect(url_for("user_movies", user_id=user_id))
            except SQLAlchemyError as e:
                flash("Database error while updating movie.", "error")
                print("Database error:", e)
                return render_template('500.html'), 500

        return render_template("update_movie.html", movie=movie, user_id=user_id)
    except Exception as e:
        flash("An unexpected error occurred.", "error")
        print("Unexpected error:", e)
        return render_template("500.html"), 500


@app.route("/movies/<int:user_id>/delete_movie/<int:movie_id>", methods=["POST"])
def delete_movie(user_id, movie_id):
    try:
        movie = data_manager.get_movie(movie_id)
        if not movie:
            flash("Movie not found.", "error")
            return jsonify({"message": "Movie not found"}), 404

        data_manager.delete_movie(movie_id)
        flash("Movie deleted successfully!", "success")
        return redirect(url_for("user_movies", user_id=user_id))

    except SQLAlchemyError as e:
        flash("Database error while deleting movie.", "error")
        print("Database error:", e)
        return render_template('500.html'), 500

    except Exception as e:
        flash("An unexpected error occurred.", "error")
        print("Unexpected error:", e)
        return render_template("500.html"), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Make sure the database and tables are created
    app.run(debug=True)