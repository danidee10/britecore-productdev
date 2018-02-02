"""Utility functions."""

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from .models import db


def create_dropdb(uri):
    """Creates/drop database if it exists."""
    engine = create_engine(uri)

    if database_exists(engine.url):
        print('Preparing to drop existing database...')
        drop_database(engine.url)
        print('Dropped Database.')

    print('Creating Database...')
    create_database(engine.url)
    print('Finished creating Database.')

    print('Initializing database')
    db.create_all()
    print('Done...App is ready')

    return engine


def dropdb(uri):
    """Drop the database."""
    print('Dropping Database...')
    drop_database(uri)
    print('Dropped Database.')