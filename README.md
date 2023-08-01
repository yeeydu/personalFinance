A personal finance project made with Flask, SQLAlchemy ORM and Chart.js. A CRUD for all expenses records, a create and delete for incomes and categories.


This is my CS50X Final Project

# PERSONAL FINANCE
#### Video Demo:  <https://youtu.be/wbyZGFEPH_o>

#### Description:
A Personal Finance Flask Project with MYSQL Database and SQLAlchemy ORM.
This small software will record all your incomes and expenses, Showing the balance according to the expenses and revenues. It also have a basic Chart to see you finance statistics. 
Project includes Python, JavaScript and SQL also bootstrap for styling

#### Project especificativos
To start the project you will have to create a database in MYSQL called personalFinance. It is set ass root with no password. After that it will only need to start a run the database. 
“If you prefer you can set a password and change it in the project .env file”.

mysql.server start
mysql -u root -p
Create database personalFinance

The project includes a requirement.txt file.
 A requirements file is documenting what Python packages are required to run the project. It will later on be used by Docker for instance to install these dependencies and ensure our application will run smoothly upon deployement with:

	pip install -r requirements.txt

This are the projects Packages I installed:
	▪	pip install SQLAlchemy
	▪	pip install python-dotenv
	▪	pip install flask-login
	▪	pip install flask-paginate
	▪	pip freeze > requirements.txt

#### Run Project
To run the project you will have to create and environment and activate it

	python3 -m venv .venv
	. .venv/bin/activate

The SQLAlchemy - create_all()  in index.py will create all tables for the project configured in the models folder. 
Because it was set in index.py you will have to run:
 	  python index.py

There’s is personalFinance.py file in the routes folder that contains all routes and logic for the application.

—
If flask project takes long and shows HTTP ERROR 403
clearing browser cookies solves the problem.
—

#### Versions:
Python 3.9.12
Flask 2.3.2
Werkzeug 2.3.6
SQLAlchemy 2.0.19
