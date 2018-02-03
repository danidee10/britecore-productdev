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
    name = db.Column(db.String(100), unique=True)

    def __str__(self):
        """User friendly name for the model."""
        return self.name


class RiskTemplate(BaseModel):
    """
    Risk templates stores the base template for each risk type.

    Stores info about different risk types E.g Automobiles and houses.
 
    Each Risk type has varying fields that are stored using JSON
    (PostgreSQL JSONB to be specific) This allows us to add arbitrary
    attributes on the fly and query them easily
   
    The main difference between RiskTemplate and RiskClient is that
    the RiskTemplate stores no values in it's JSONB columns
    it only stores a column's metadata It can be used to update
    existing Risk records when a new column is added or removed.

    Risk records are records that are tied to clients for each Insurer
    """

    insurer_id = db.Column(
        db.Integer, db.ForeignKey('insurer.id'), nullable=False
    )

    insurer = db.relationship(
        Insurer, backref=db.backref('risk_templates', lazy=True)
    )

    name = db.Column(db.String(60))
    fields = db.Column(JSONB)

    def __str__(self):
        """User friendly representation of the risk template."""
        return self.name

    def to_json(self):
        """Returns dict representation that can be jsonified."""
        return {
            'id': self.id,
            'name': self.name,
            'fields': self.fields
        }


class RiskClient(BaseModel):
    """
    This is the actual model that stores info for different clients
    """

    risk_template_id = db.Column(
        db.Integer, db.ForeignKey('risk_template.id'), nullable=False
    )

    risk_template = db.relationship(
        RiskTemplate, backref=db.backref('risks', lazy=True)
    )

    fields = db.Column(JSONB)

    def __str__(self):
        """Return the customer name as the str representation."""
        customer_name = filter(
            lambda x: x['name'] == 'Customer Name', self.fields
        )
        return next(customer_name)["value"]
