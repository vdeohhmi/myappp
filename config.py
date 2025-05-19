import os
from os import path

BASE_DIR = path.abspath(path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'sqlite:///' + path.join(BASE_DIR, 'instance', 'app.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
