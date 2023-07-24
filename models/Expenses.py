from flask import app
from sqlalchemy import func
from datetime import datetime
from data.db import db

# once we create our first record it will create the database
class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Numeric(20), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, item,  category, value, created_at):
        self.item = item
        self.category = category
        self.value = value
        self.created_at = created_at

    # def __repr__(self):
    #     return '<Expenses %r>' % self.id

