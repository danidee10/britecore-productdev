"""Configuration file."""

from os import environ

DEBUG = True
SECRET_KEY = environ.get('SECRET_KEY', 'localsecret')

SQLALCHEMY_DATABASE_URI = environ.get(
    'DATABASE_URL', 'postgresql://postgres@localhost/britecore'
)
SQLALCHEMY_TRACK_MODIFICATIONS = True
