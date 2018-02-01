"""SQLAlchemy models."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql.json import JSONB


db = SQLAlchemy()


class BaseModel(db.Model):
    """Base model that implements some basic fields needed in other models."""
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp()
    )


class Insurer(BaseModel):
    """Model to store Insurer data."""
    name = db.Column(db.String)


class Risk(BaseModel):
    """
    Stores info about different risk types E.g Automobiles and houses.
  
    Each Risk type has varying fields that are stored using JSON
    (PostgreSQL JSONB to be specific) This allows us to add arbitrary
    attributes on the fly and query them easily
    """

    insurer_id = db.Column(
        db.Integer, db.ForeignKey('insurer.id'), nullable=False
    )

    insurer = db.relationship(Insurer, backref=db.backref('risks', lazy=True))

    risk_type = db.Column(db.String)
    fields = db.Column(JSONB)

    def to_json(self):
        """Returns dict representation that can be jsonified."""
        return {
            'type': self.risk_type,
            'fields': self.fields
        }