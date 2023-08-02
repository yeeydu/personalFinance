# PERSONAL FINANCE
A personal finance project made with Flask, SQLAlchemy ORM and Chart.js. A CRUD for all expenses records, a create and delete for incomes and categories.


This is my CS50X Final Project

# PERSONAL FINANCE
#### Video Demo:  <https://youtu.be/wbyZGFEPH_o>
#### Description:
A Personal Finance Flask Project with MYSQL Database and SQLAlchemy ORM.
This small software will record all your incomes and expenses, Showing the balance according to the expenses and revenues. A CRUD method for expenses and income, paginations and responsive.
It also have a basic Chart to see you finance statistics. 
Project was done with Flask Python framwork, JavaScript and MySQL also bootstrap for styling.
---

**Project especificativos**
To start the project you will have to create a database in MYSQL called personalFinance. It is set ass root with no password. After that it will only need to start a run the database. 

`MYSQL_USER` = root

`MYSQL_PASSWORD` = 

`MYSQL_DATABASE` = personalFinance

`MYSQL_HOST` = localhost
 

“If you prefer you can set a password and change it in the project .env file” then it will link to the app.py database connection with thouse variables.

```bash
	mysql.server start
	mysql -u root -p
	Create database personalFinance
```

**The project includes a requirement.txt file.**
 A requirements file is documenting what Python packages are required to run the project. It will later on be used by Docker for instance to install these dependencies and ensure our application will run smoothly upon deployement with:

	pip install -r requirements.txt

**This are the projects Packages I installed:**
```bash
		pip install SQLAlchemy
		pip install python-dotenv
		pip install flask-login
		pip install flask-paginate
		pip freeze > requirements.txt
```

**Run Project**
To run the project you will have to create and environment and activate it
```bash
	python3 -m venv .venv
	. .venv/bin/activate
```

**SQLAlchemy**
The SQLAlchemy - create_all()  in index.py will create all tables for the project configured in the models folder. 
Because it was set in index.py you will have to run:

```bash
	python index.py
```

**Main file**
There’s is personalFinance.py file in the routes folder that contains all routes and logic for the application.

**Info**
If flask project takes long and shows HTTP ERROR 403
clearing browser cookies solves the problem.

## Stack used

**Front-end:** HTML, CSS, BOOTSTRAP, JAVASCRIPT

**Back-end:** FLASK, JAVASCRIPT, MYSQL

## Funcionalities

- CRUD
- Realtime charts
- Responsive
- Multiple users

**Packages Version:**
- Python 3.9.12
- Flask 2.3.2
- Werkzeug 2.3.6
- SQLAlchemy 2.0.19

## Screenshots

![App Screenshot](<img src="/static/thumb.png" alt="example" title="example">)

## 🔗 Links
[![portfolio](https://img.shields.io/badge/my_portfolio-000?style=for-the-badge&logo=ko-fi&logoColor=white)](https://yeeysonduarte.vercel.app/)
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yeeyson-duarte-6545041a7/)