from app import app
from data.db import db


# create tables define in the model when program starts
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)  # prevent to stop and run each tim
