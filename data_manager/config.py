import os
import dotenv

dotenv.load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'database.db')}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

OMDB_API_KEY = os.getenv("API_KEY")

SECRET_KEY = os.getenv("SECRET_KEY", "secret_key")