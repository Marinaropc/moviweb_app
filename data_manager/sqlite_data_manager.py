from data_manager.data_manager_interface import DataManagerInterface
from data_manager.models import db, User, Movie

class SQLiteDataManager(DataManagerInterface):
    """Manages all database operations using SQLAlchemy."""

    def get_all_users(self):
        """Retrieve all users from the database."""
        return User.query.all()


    def get_user_movies(self, user_id):
        """Retrieve all movies associated with a given user."""
        return Movie.query.filter_by(user_id=user_id).all()


    def get_movie(self, movie_id):
        movie = Movie.query.get(movie_id)
        return movie


    def get_user(self, user_id):
        user = User.query.get(user_id)
        return user


    def add_user(self, name):
        """Add a new user to the database."""
        user = User(name = name)
        db.session.add(user)
        db.session.commit()
        return user


    def add_movie(self, user_id, name, director, year, rating, poster):
        """Add a new movie to the database."""
        movie = Movie(user_id=user_id, name=name, director=director,
                      year=year, rating=rating, poster=poster)
        db.session.add(movie)
        db.session.commit()
        return movie


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
            db.session.commit()
            return movie
        return None


    def delete_movie(self, movie_id):
        """Delete a movie from the database."""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        movie_not_found = False
        return movie_not_found
