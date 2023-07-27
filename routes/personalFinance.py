from collections import Counter
import datetime
from functools import wraps
from flask import (
    Blueprint,
    Flask,
    request,
    render_template,
    url_for,
    redirect,
    flash,
    session,
)
from flask_login import current_user
from flask_session import Session
from models.Expenses import Category, Expenses
from data.db import db
from sqlalchemy import Connection, Null, engine_from_config, func, select, text
from werkzeug.security import generate_password_hash, check_password_hash
from models.Income import Income, Income_type
from models.Users import Users

personalFinance = Blueprint("personalFinance", __name__)


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# ROUTES
@personalFinance.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        category = request.form.get("category")
        income_type = request.form.get("income_type")

        # Save Expenses
        if category:
            # category = Category.query.all()
            item = request.form.get("item")
            category = request.form.get("category")
            value = request.form.get("value")
            created_at = datetime.datetime.now()

            newExpence = Expenses(item, category, value, created_at)
            db.session.add(newExpence)

            # if no value is selected gives error message
            if not item or not category or not value:
                message = "You must fill all information"
                return render_template("error.html", message=message)

            db.session.commit()

            # Flash message of success
            flash("Expense added succesfully!")

            # Redirect user to home page
            return redirect("/")

        # Save income
        if income_type:
            # income = Income.query.all()

            income_type = request.form.get("income_type")
            value = request.form.get("value")
            created_at = datetime.datetime.now()

            newIncome = Income(income_type, value, created_at)
            db.session.add(newIncome)

            # if no value is selected gives error message
            if not value:
                message = "You must fill the value"
                return render_template("error.html", message=message)
            if income_type is None:
                message = "You must create a income type"
                return render_template("error.html", message=message)

            db.session.commit()

            # Flash message of success
            flash("Income added succesfully!")

            # Redirect user to home page
            return redirect("/")

    else:
        user_id = session["user_id"]
        # user = Expenses.query.filter(Expenses.user_id == user_id).first()
        # info = Expenses.select(Expenses.item, Expenses.value).where(Expenses.user_id == user_id)
        # expenses = db.session("select * FROM Expenses WHERE expenses.user_id= ?", user_id)

        income = Income.query.all()
        income_type = Income_type.query.all()
        #sum total income
        total_income = Income.query.with_entities(func.sum(Income.value).label('total')).first().total

        expenses = Expenses.query.all()
        category = Category.query.all()
        #sum total expenses
        total_expenses = Expenses.query.with_entities(func.sum(Expenses.value).label('total')).first().total

        catId = Category.query.all()
        #balance
        if total_income is None:
            total_income = 0
        if total_expenses is None:
            total_expenses = 0
        balance = total_income - total_expenses

        return render_template(
            "index.html",
            expenses=expenses,
            category=category,
            catId=catId,
            income=income,
            income_type=income_type,
            total_income=total_income,
            total_expenses=total_expenses,
            balance=balance
        )


# UPDATE EXPENSES METHOD
@personalFinance.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    if request.method == "POST":
        expenses = Expenses.query.get(id)
        expenses.item = request.form.get("item")
        expenses.category = request.form.get("category")
        expenses.value = request.form.get("value")

        db.session.commit()

        # Flash message of success
        flash("Expense updated succesfully!")

        # Redirect user to home page
        return redirect("/")

    else:
        expenses = Expenses.query.get(id)
        return render_template("update.html", expenses=expenses)


# DELETE METHOD
@personalFinance.route("/delete/<id>", methods=["POST"])
@login_required
def delete(id):
    id = Expenses.query.get(id)
    db.session.delete(id)
    db.session.commit()

    # Flash message of success
    flash("Expense Deleted!")

    # Redirect user to home page
    return redirect("/")


@personalFinance.route("/delete_income/<id>", methods=["POST"])
@login_required
def delete_income(id):
    id = Income.query.get(id)
    db.session.delete(id)
    db.session.commit()

    # Flash message of success
    flash("Income Deleted!")

    # Redirect user to home page
    return redirect("/")


# REGISTRATION
@personalFinance.route("/registration", methods=["GET", "POST"])
def register():
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")

        # Ensure passwords are the same
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not request.form.get("username"):
            message = "You must provide username"
            return render_template("error.html", message=message)

        # Ensure password was submitted
        elif not request.form.get("password"):
            message = "You must provide password"
            return render_template("error.html", message=message)

        # Ensure password was re-submitted
        elif not request.form.get("confirmation"):
            message = "You must confirm password"
            return render_template("error.html", message=message)
        elif password != confirmation:
            message = "Password and confirm password must be the same"
            return render_template("error.html", message=message)

        # hash user password
        hash = generate_password_hash(password)

        # Query database for username
        user = Users.query.filter_by(username=username).first()

        # Ensure username is not duplicated
        if user:
            message = "User already exist"
            return render_template("error.html", message=message)

        # insert user into database
        created_at = datetime.datetime.now()

        newUser = Users(username, hash, created_at)
        db.session.add(newUser)
        db.session.commit()

        # Remember which user has register in
        session["user_id"] = newUser

        # Flash message of success
        flash("New user register succesfully!")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")


# @personalFinance.route("/contact", methods=["GET"])
# def contact():
#     return render_template("contact.html")


# LOGIN
@personalFinance.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username", "guest"):
            message = "You must provide username"
            return render_template("error.html", message=message)

        # Ensure password was submitted
        elif not request.form.get("password", ""):
            message = "You must provide password"
            return render_template("error.html", message=message)

        # Query database for username
        username = request.form.get("username")
        password = request.form.get("password")

        user = Users.query.filter_by(username=username).first()

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user or not check_password_hash(user.password, password):
            message = "Invalid username and/or password"
            return render_template("error.html", message=message)

        # Remember which user has logged in
        session["user_id"] = user

        # Redirect user to home page
        return redirect("/")
        # return render_template("index.html", username=user.username)

    # User reached route via GET
    else:
        return render_template("login.html")


@personalFinance.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# SAVE NEW CATEGORIES PAGE
@personalFinance.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    if request.method == "POST":
        category = request.form.get("category")
        income_type = request.form.get("income_type")

        # category
        if category:
            # category = Category(name="Housing")
            # session.add(category)

            category = request.form.get("category")
            newCategory = Category(category)
            db.session.add(newCategory)

            if not category:
                message = "You must fill a category"
                return render_template("error.html", message=message)

            db.session.commit()
            flash("Category added succesfully!")
            # Redirect user to home page
            return redirect("/categories")

        # income type
        if income_type:
            income_type = request.form.get("income_type")
            newType = Income_type(income_type)
            db.session.add(newType)

            if not income_type:
                message = "You must fill a income type"
                return render_template("error.html", message=message)

            db.session.commit()
            flash("Income type added succesfully!")
            # Redirect user to home page
            return redirect("/categories")

    else:
        category = Category.query.all()
        income_type = Income_type.query.all()
        return render_template(
            "categories.html", category=category, income_type=income_type
        )



#         # get user cash balance
#         balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
#         balance_cash = balance[0]["cash"]

#         # update user database with the new balance
#         new_balance = balance_cash + float(add)
#         db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, user_id)

