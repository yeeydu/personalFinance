from flask import app
from sqlalchemy import func
from datetime import datetime
from data.db import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __init__(self, name, password, created_at):
        self.name = name
        self.password = password
        self.created_at = created_at
