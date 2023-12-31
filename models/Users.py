from flask import app
from sqlalchemy import func
from datetime import datetime
from data.db import db
from werkzeug.security import generate_password_hash


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # income_type = db.relationship('Income_type', secondary=users_income, primaryjoin="User.id == Income.users_id", backref='users') #
    # expenses = db.relationship('Expenses', secondary=users_expenses, primaryjoin="User.id == Expenses.users_id", backref='users') #

    def __init__(self, username, password, created_at):
        self.username = username
        self.password = password
        self.created_at = created_at
