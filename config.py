import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def database_url():
    """Return a SQLAlchemy URL compatible with Render PostgreSQL and psycopg."""
    value = os.environ.get("DATABASE_URL")
    if not value:
        return f"sqlite:///{BASE_DIR / 'instance' / 'edumanage.db'}"
    if value.startswith("postgres://"):
        value = "postgresql://" + value.removeprefix("postgres://")
    if value.startswith("postgresql://"):
        return "postgresql+psycopg://" + value.removeprefix("postgresql://")
    return value

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.environ.get("FLASK_ENV") == "production"
    WTF_CSRF_TIME_LIMIT = 3600
