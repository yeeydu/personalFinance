from functools import wraps
from flask import Flask, request, render_template, session, redirect
from config import DATABASE_CONNECTION_URI
from routes.personalFinance import personalFinance
from flask_sqlalchemy import SQLAlchemy
from models.Expenses import Expenses
from data.db import db
from flask_session import Session

# create the app
app = Flask(__name__)

app.secret_key = "secret key"

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Delete cookies
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    response.set_cookie('username', path='/', expires=0)
    return response


# db = SQL("sqlite:///personalFinance.db")
# LINK TO DATABASE "sqlite:///project.db"
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# SQLAlchemy(app)
db.init_app(app)

# importing all routes form route folder personalFinance file, with blueprint
app.register_blueprint(personalFinance)


# use locale for conversion in Flask code
@app.template_filter("conv_curr")
def conv_curr(amount):
    import locale

    locale.setlocale(locale.LC_ALL, "en_US.UTF-8")
    return locale.currency(amount)
