import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "mountainrent-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.path.dirname(BASE_DIR),
        "instance",
        "database.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEFAULT_ADMIN_EMAIL = "admin@mountainrent.com"
    DEFAULT_ADMIN_PASSWORD = "admin123"