"""Main app file."""

from flask import Flask, jsonify, render_template, request

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

from .models import db, Risk
from .admin import admin
from .config import config as CONFIG


app = Flask(__name__)
app.config.from_object(CONFIG)

db.init_app(app)
admin.init_app(app)


@app.cli.command('createdb')
def create_dropdb():
    """Creates/drop database if it exists."""
    engine = create_engine(CONFIG.SQLALCHEMY_DATABASE_URI)

    if database_exists(engine.url):
        app.logger.info('Preparing to drop existing database...')
        drop_database(engine.url)
        app.logger.info('Dropped Database.')

    app.logger.info('Creating Database...')
    create_database(engine.url)
    app.logger.info('Finished creating Database.')

    app.logger.info('Initializing database')
    db.create_all()
    app.logger.info('Done...App is ready')

    return engine


@app.cli.command()
def dropdb():
    """Drop the database."""
    app.logger.info('Dropping Database...')
    drop_database(CONFIG.SQLALCHEMY_DATABASE_URI)
    app.logger.info('Dropped Database.')



@app.route('/')
def home():
    """Renders the Single Page Application."""

    return render_template('index.html')


@app.route('/risks/', defaults={'risk_id': None})
@app.route('/risks/<int:risk_id>/')
def get_risk_by_id(risk_id):
    """Endpoint for risks."""
    if risk_id:
        risk = db.session.query(Risk).get(risk_id)
        return jsonify(risk.to_json())

    risks = db.session.query(Risk).all()
    risks = [risk.to_json() for risk in risks]

    return jsonify(risks)


@app.teardown_request
def close_db_connection(exception=None):
    """Closes the db connection at the end of each request."""
    db.session.remove()
