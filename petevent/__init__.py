from flask_sqlalchemy import SQLAlchemy
from cs50 import SQL
from flask import Flask

app = Flask(__name__)

# Configure SQLAlchemy to use SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///pets.db"
db_alchemy = SQLAlchemy(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///petevent/pets.db")

from petevent import routes
from petevent.errors.handlers import errors

app.register_blueprint(errors)
