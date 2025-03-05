from flask_sqlalchemy import SQLAlchemy

from data_manager_interface import DataManagerInterface
from models import db, User, Movie

class SQLiteDataManager(DataManagerInterface):
    """Manages all database operations using SQLAlchemy."""

    def get_all_users(self):
        """Retrieve all users from the database."""
        return User.query.all()

    def get_user_movies(self, user_id):
        """Retrieve all movies associated with a given user."""
        return Movie.query.filter_by(user_id=user_id).all()

    @staticmethod
    def add_user(self, name):
        """Add a new user to the database."""
        user = User(name = name)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def add_movie(self, name, director, year, rating, user_id):
        """Add a new movie to the database."""
        movie = Movie(name = name, director = director, year = year,
                      rating = rating, user_id = user_id)
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, name = None, director = None,
                     year = None, rating = None):
        """Update an existing movie's details."""
        movie = Movie.query.get(movie_id)
        if movie:
            if name:
                movie.name = name
            if director:
                movie.director = director
            if year:
                movie.year = year
            if rating:
                movie.rating = rating

