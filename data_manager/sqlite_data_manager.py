from data_manager.data_manager_interface import DataManagerInterface
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
    def get_movie(movie_id):
        movie = Movie.query.get(movie_id)
        return movie

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        return user

    @staticmethod
    def add_user(name):
        """Add a new user to the database."""
        user = User(name = name)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def add_movie(user_id, name, director, year, rating):
        """Add a new movie to the database."""
        movie = Movie(user_id=user_id, name=name, director=director,
                      year=year, rating=rating)
        db.session.add(movie)
        db.session.commit()
        return movie

    @staticmethod
    def update_movie( movie_id, name = None, director = None,
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
            db.session.commit()
            return movie
        return None

    @staticmethod
    def delete_user(user_id):
        """Delete a user from the database."""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        user_not_found = False
        return user_not_found

    @staticmethod
    def delete_movie(movie_id):
        """Delete a movie from the database."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        movie_not_found = False
        return movie_not_found
