import os
from os.path import dirname, join

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# load env
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("database")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
