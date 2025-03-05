from flask import Flask
from sqlite_data_manager import SQLiteDataManager
from models import db, User, Movie
import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# Instantiate the DataManager
data_manager = SQLiteDataManager()

@app.route('/add_user/<name>')
def add_user(name):
    data_manager.add_user(name)
    return f"User {name} added successfully!"

@app.route('/add_movie/<user_id>/<name>/<director>/<int:year>/<float:rating>')
def add_movie(user_id, name, director, year, rating):
    data_manager.add_movie(user_id, name, director, year, rating)
    return f"Movie {name} added for User {user_id}!"

@app.route('/get_users')
def get_users():
    users = data_manager.get_all_users()
    return f"Users: {[user.name for user in users]}"

@app.route('/get_user_movies/<user_id>')
def get_user_movies(user_id):
    movies = data_manager.get_user_movies(user_id)
    return f"Movies for User {user_id}: {[movie.name for movie in movies]}"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Make sure the database and tables are created
    app.run(debug=True)