"""Configuration for local development."""

DEBUG = True
SECRET_KEY = 'localsecret'

SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/britecore'
SQLALCHEMY_TRACK_MODIFICATIONS = True
