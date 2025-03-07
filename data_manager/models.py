from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(100), nullable=False)
    movies = db.relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name})"


class Movie(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(255), nullable=True)
    year = db.Column(db.String(4), nullable=True)
    rating = db.Column(db.String(5), nullable=True)
    poster = db.Column(db.String(512), nullable=True)


    def __repr__(self):
        return f"User(id = {self.id}, name = {self.name}, director = {self.director}, year = {self.year}, rating = {self.rating})"