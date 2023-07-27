from flask import app
from sqlalchemy import func
from datetime import datetime
from data.db import db
from sqlalchemy.orm import relationship

# once we create our first record it will create the database
class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    item = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id', ondelete="CASCADE"))
    value = db.Column(db.Numeric(8,2), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # user = db.relationship("Users", db.foreignkeys="[user.id]")
    # category = db.relationship("Category", db.foreignkeys="[category.id]")

    def __init__(self, item,  category, value, created_at):
        self.item = item
        self.category = category
        self.value = value
        self.created_at = created_at

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), nullable=False)

    def __init__(self, category):
        self.category = category


    # def __repr__(self):
    #     return '<Expenses %r>' % self.id

