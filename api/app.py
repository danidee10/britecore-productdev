"""Main app file."""

from flask import Flask, abort, jsonify, make_response, render_template

from flask_cors import CORS

from .admin import admin
from .config import config as CONFIG
from .utils import create_dropdb, dropdb
from .models import db, RiskTemplate


app = Flask(
    __name__, template_folder='../frontend/dist',
    static_folder='../frontend/dist/static'
)
app.config.from_object(CONFIG)

db.init_app(app)
admin.init_app(app)

# Enable CORS (It's not necessary if Flask serves the Vue app)
CORS(app)


@app.cli.command('createdb')
def create_drop_database():
    """Create or drop database if it exists."""
    create_dropdb(CONFIG.SQLALCHEMY_DATABASE_URI)


@app.cli.command()
def drop_database():
    """Drop the database."""
    dropdb(CONFIG.SQLALCHEMY_DATABASE_URI)


@app.route('/')
def home():
    """Renders the Single Page Application."""

    return render_template('index.html')


@app.route('/risks/')
def get_risks():
    """Get all risks."""
    risks = db.session.query(RiskTemplate).all()
    risks = [risk.to_json() for risk in risks]

    return jsonify(risks)


@app.route('/risks/<int:risk_id>/')
def get_risk_by_id(risk_id):
    """Get a risk by it's id."""
    risk = db.session.query(RiskTemplate).get(risk_id)

    if not risk:
        abort(make_response(jsonify({'message': 'Risk not found'}), 404))

    return jsonify(risk.to_json())      


@app.teardown_request
def close_db_connection(exception=None):
    """Closes the db connection at the end of each request."""
    db.session.close()
