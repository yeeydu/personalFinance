from collections import Counter
import datetime
from functools import wraps
import json
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
from flask_login import current_user, login_user
from flask_session import Session
import sqlalchemy
from models.Expenses import Category, Expenses
from data.db import db
from sqlalchemy import (
    Connection,
    Engine,
    MetaData,
    Null,
    engine_from_config,
    func,
    select,
    text,
)
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


""" ROUTES  """


# INDEX
@personalFinance.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        category = request.form.get("category")
        income_type = request.form.get("income_type")

        # Save Expenses
        if category:
            user_id = session["user_id"]

            item = request.form.get("item")
            category = request.form.get("category")
            value = request.form.get("value")
            created_at = datetime.datetime.now()

            newExpence = Expenses(user_id.id, item, category, value, created_at)
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
            user_id = session["user_id"]

            income_type = request.form.get("income_type")
            value = request.form.get("value")
            created_at = datetime.datetime.now()

            newIncome = Income(user_id.id, income_type, value, created_at)
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
        # expenses = db.session("select * FROM Expenses WHERE expenses.user_id= ?", user_id)

        income = Income.query.filter(Income.users_id == user_id.id).limit(4).all()
        income_type = Income_type.query.filter(Income_type.users_id == user_id.id).all()

        # sum total income
        total_income = (
            Income.query.filter(Income.users_id == user_id.id)
            .with_entities(func.sum(Income.value).label("total"))
            .first()
            .total
        )
        # pagination
        page = request.args.get("page", 1, type=int)
        pagination = Expenses.query.filter(Expenses.users_id == user_id.id).paginate(
            page=page, per_page=5
        )

        # expenses = Expenses.query.limit(5).all()
        #category = Category.query.filter(Expenses.users_id == user_id.id).all()
        category = Category.query.filter(Category.users_id == user_id.id).all()

        # sum total expenses
        total_expenses = (
            Expenses.query.filter(Expenses.users_id == user_id.id)
            .with_entities(func.sum(Expenses.value).label("total"))
            .first()
            .total
        )

        # balance
        if total_income is None:
            total_income = 0
        if total_expenses is None:
            total_expenses = 0
        balance = total_income - total_expenses

        return render_template(
            "index.html",
            # expenses=expenses,
            category=category,
            income=income,
            income_type=income_type,
            total_income=total_income,
            total_expenses=total_expenses,
            balance=balance,
            pagination=pagination,
            user_id=user_id.username,
        )


# EXPENSES LIST PAGE
@personalFinance.route("/expenses/<int:page_num>", methods=["GET"])
@login_required
def expenses(page_num):
    user_id = session["user_id"]
    page = request.args.get("page", 1, type=int)
    pagination = Expenses.query.filter(Expenses.users_id == user_id.id).paginate(
        page=page_num, per_page=10, error_out=True
    )
    category = Category.query.all()
    return render_template("expenses.html", pagination=pagination, category=category)


# UPDATE EXPENSES METHOD
@personalFinance.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update(id):
    if request.method == "POST":
        user_id = session["user_id"]
        category = Category.query.get(id)
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
        category = Category.query.all()
        expenses = Expenses.query.get(id)
        return render_template("update.html", expenses=expenses, category=category)


# DELETE EXPENSES METHOD
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


# SAVE NEW CATEGORIES PAGE
@personalFinance.route("/categories", methods=["GET", "POST"])
@login_required
def categories():
    if request.method == "POST":
        category = request.form.get("category")
        income_type = request.form.get("income_type")

        # category = expenses category
        if category:
            user_id = session["user_id"]
            # category = Category(name="Housing")
            # session.add(category)

            category = request.form.get("category")
            newCategory = Category(user_id.id, category)
            db.session.add(newCategory)

            if not category:
                message = "You must fill a category"
                return render_template("error.html", message=message)

            db.session.commit()
            flash("Category added succesfully!")
            # Redirect user to home page
            return redirect("/categories")

        # income type category
        if income_type:
            user_id = session["user_id"]
            income_type = request.form.get("income_type")
            newType = Income_type(user_id.id, income_type)
            db.session.add(newType)

            if not income_type:
                message = "You must fill a income type"
                return render_template("error.html", message=message)

            db.session.commit()
            flash("Income type added succesfully!")
            # Redirect user to Categories page
            return redirect("/categories")

    else:
        user_id = session["user_id"]
        category = Category.query.filter(Category.users_id == user_id.id).all()
        income_type = Income_type.query.filter(Income_type.users_id == user_id.id).all()
        return render_template(
            "categories.html", category=category, income_type=income_type
        )


# INCOME LIST PAGE
@personalFinance.route("/income/<int:page_num>", methods=["GET"])
@login_required
def income(page_num):
    user_id = session["user_id"]
    page = request.args.get("page", 1, type=int)
    income = Income.query.filter(Income.users_id == user_id.id).paginate(
        page=page_num, per_page=10, error_out=True
    )
    income_type = Income_type.query.all()
    return render_template("income.html", income=income, income_type=income_type)


# to keep it simple with incomes i just create and delete incomes
# DELETE INCOME METHOD
@personalFinance.route("/delete_income/<id>", methods=["POST"])
@login_required
def delete_income(id):
    user_id = session["user_id"]
    id = Income.query.get(id)
    db.session.delete(id)
    db.session.commit()

    # Flash message of success
    flash("Income Deleted!")

    # Redirect user to home page
    return redirect("/")


# DELETE CATEGORY METHOD
@personalFinance.route("/delete_category/<id>", methods=["POST"])
@login_required
def delete_category(id):
    user_id = session["user_id"]
    id = Category.query.get(id)
    db.session.delete(id)
    db.session.commit()

    # Flash message of success
    flash("Category Deleted!")

    # Redirect user to home page
    return redirect("/categories")


# DELETE INCOME_TYPE METHOD
@personalFinance.route("/delete_income_type/<id>", methods=["POST"])
@login_required
def delete_income_type(id):
    user_id = session["user_id"]
    id = Income_type.query.get(id)
    db.session.delete(id)
    db.session.commit()

    # Flash message of success
    flash("Income type Deleted!")

    # Redirect user to home page
    return redirect("/categories")


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
        return redirect("/login")

    # User reached route via GET
    else:
        return render_template("register.html")


# DASHBOARD
@personalFinance.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    # ...

    user_id = session["user_id"]

    # Define date
    today = datetime.datetime.now()
    month = today.month
    year = today.year

    # total_income per month
    total_income = (
        Income.query.filter(Income.users_id == user_id.id)
        .filter(
            db.and_(
                Income.created_at
                > datetime.date(year=today.year, month=today.month, day=today.day)
            )
        )
        .with_entities(func.sum(Income.value).label("total"))
        .first()
        .total
    )
    # total_expenses per month
    total_expenses = (
        Expenses.query.filter(Expenses.users_id == user_id.id)
        .filter(
            db.and_(
                Expenses.created_at
                > datetime.date(year=today.year, month=today.month, day=today.day)
            )
        )
        .with_entities(func.sum(Expenses.value).label("total"))
        .first()
        .total
    )

    # sqlalchemy.select([
    #     Expenses.item,
    #     sqlalchemy.func.count(Expenses.category)
    # ]).group_by(Expenses.category)

    # Write a SQL query using groupby for feature fixe
    # cat = Expenses.query.filter(Expenses.users_id == user_id.id).filter(db.and_(Expenses.created_at > datetime.date(year=today.year, month=today.month, day=today.day))).with_entities(func.sum(Expenses.value)).group_by(Expenses.category).all()

    # query month expenses for graphic
    expenses = (
        Expenses.query.filter(Expenses.users_id == user_id.id)
        .filter(
            db.and_(
                Expenses.created_at
                > datetime.date(year=today.year, month=today.month, day=today.day)
            )
        )
        .all()
    )
    item = []
    value = []
    category = []
    for expense in expenses:
        item.append(expense.item)
        value.append(expense.value)
        category.append(expense.category)

    if total_income is None:
        total_income = 0
    if total_expenses is None:
        total_expenses = 0
    month_balance = total_income - total_expenses

    # query year expenses for graphic
    allExpenses = (
        Expenses.query.filter(Expenses.users_id == user_id.id)
        .filter(db.and_(Expenses.created_at >= year))
        .all()
    )
    year_item = []
    year_value = []
    year_category = []
    for allExpenses in allExpenses:
        year_item.append(allExpenses.item)
        year_value.append(allExpenses.value)
        year_category.append(allExpenses.category)

    return render_template(
        "dashboard.html",
        total_income=(total_income),
        total_expenses=(total_expenses),
        expenses=expenses,
        item=(item),
        value=(value),
        category=category,
        user_id=user_id.username,
        month_balance=month_balance,
        allExpenses=allExpenses,
        year_item=year_item,
        year_value=year_value,
        year_category=year_category,
    )


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

        # Flash message of success
        flash("Login succesfully!")

        # Redirect user to home page
        return redirect("/")
        # return render_template("index.html", username=user.username)

    # User reached route via GET
    else:
        return render_template("login.html")


"""
@personalFinance.route("/password", methods=["GET", "POST"])
@login_required
def password():
# Change password 
    if request.method == "POST":
        # Ensure passwords are the same
        user_id = session["user_id"]
        username = request.form.get("password")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not request.form.get("username"):
            message = "You must provide your username"
            return render_template("error.html", message=message)

        # Ensure password was submitted
        if not request.form.get("password", ""):
            message = "You must provide password"
            return render_template("error.html", message=message)

        # Ensure password was re-submitted
        elif not request.form.get("confirmation"):
            message = "You must confirm password"
            return render_template("error.html", message=message)
        elif password != confirmation:
            message = "Password and confirm password must be the same"
            return render_template("error.html", message=message)

        user = Users.query.filter_by(username=Users.username).all()
        print(user)
        # insert user into database
        try:
            # hash user password
            newPass = generate_password_hash(password)

            Users.query.filter_by(user).update(dict(password=newPass))
            db.session.commit()
            # sqlalchemy.execute('UPDATE users SET password =? WHERE id = ?', newPass, user_id)

            # Flash message of success
            flash("New password register succesfully!")
        except:
            message = "An error acurred"
            return render_template("error.html", message=message)

        # Redirect user to login form
        return redirect("/")

    else:
        user_id = session["user_id"]
        return render_template("password.html")
"""


@personalFinance.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
