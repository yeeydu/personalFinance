from flask import app
from sqlalchemy import func
from datetime import datetime
from data.db import db
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
# once we create our first record it will create the database
# expenses_category = db.table(
#     "expenses_category",
#     db.Column('expenses_id', db.Integer, db.ForeignKey('expenses.id')),
#     db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
# )#


class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    item = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Numeric(8, 2), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    category = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"))
    #category = db.relationship('Category', secondary=expenses_category, backref='category') #
    
    # user = db.relationship("Users", db.ForeignKey="[user.id]")
    # category = db.relationship("Category", backref="expenses")# one to many relation

    def __init__(self, item, category, value, created_at):
        self.item = item
        self.category = category
        self.value = value
        self.created_at = created_at


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100), server_default="Housing", nullable=False , default="Housing")
    #expenses_id = db.relationship('Expenses', secondary=expenses_category, primaryjoin="Expenses.id == Category.expenses_id", backref='category') #

    def __init__(self, category):
        self.category = category

    # def __repr__(self):
    #     return '<Expenses %r>' % self.id
