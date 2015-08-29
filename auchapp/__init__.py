from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('auchapp.settings')
db = SQLAlchemy(app)

from auchapp import api