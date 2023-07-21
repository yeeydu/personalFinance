import re
from datetime import datetime
from flask import Flask, request, render_template


app = Flask(__name__)

    
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     #Log user in

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":
#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute(
#             "SELECT * FROM users WHERE username = ?", request.form.get("username")
#         )

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(
#             rows[0]["hash"], request.form.get("password")
#         ):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         #Redirect new user to quotes to buy shares"""
#         user_id = session["user_id"]
#         user_info = db.execute(
#             "SELECT SUM(shares)AS shares FROM transactions WHERE user_id = ? GROUP BY symbol",
#             user_id,
#         )

#         if not user_info:
#             return redirect("/index")
        
#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")


# @app.route("/balance", methods=["GET", "POST"])
# @login_required
# def balance():
#     """Get Cash balance and add some"""
#     if request.method == "POST":
#         user_id = session["user_id"]
#         add = request.form.get("add")

#         # Ensure value was submitted
#         if not add:
#             return apology("must provide some values", 403)

#         # get user cash balance
#         balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
#         balance_cash = balance[0]["cash"]

#         # update user database with the new balance
#         new_balance = balance_cash + float(add)
#         db.execute("UPDATE users SET cash = ? WHERE id = ?", new_balance, user_id)

#         return redirect("/")

#     else:
#         # get user cash balance
#         user_id = session["user_id"]
#         balance = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
#         balance_cash = balance[0]["cash"]
#         return render_template("balance.html", balance_cash=balance_cash)

        