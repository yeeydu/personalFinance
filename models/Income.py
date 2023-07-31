from flask import app
from sqlalchemy import func
from datetime import datetime
from data.db import db
from sqlalchemy.orm import relationship

# once we create our first record it will create the database
# income_income_type = db.table(
#     "income_income_type",
#     db.Column("income_id", db.Integer, db.ForeignKey("income.id")),
#     db.Column("income_type_id", db.Integer, db.ForeignKey("income_type.id")),
# )#

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"))
    income_type = db.Column(db.Integer, db.ForeignKey('income_type.id', ondelete="CASCADE"))
    value = db.Column(db.Numeric(8,2), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    #income_type_id = db.relationship('Income_type', secondary=income_income_type, primaryjoin="Income.id == Income_type.income_id", backref='income') #

    # user = db.relationship("Users", ForeignKey="[user_id]")
    # income_type = db.relationship("Income_type", ForeignKey="[income_type]")

    def __init__(self, income_type, value, created_at):
        self.income_type = income_type
        self.value = value
        self.created_at = created_at

class Income_type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    income_type = db.Column(db.String(100), server_default="Salary", nullable=False , default="Salary")
    #income_id = db.Column(db.Integer, db.ForeignKey('income.id'))#

    def __init__(self, income_type):
        self.income_type = income_type