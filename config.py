import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False

    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True

    SECRET_KEY = os.environ.get('KEY')

    # URI используемая для подключения к базе данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
