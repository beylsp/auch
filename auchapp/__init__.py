from flask import Flask

app = Flask(__name__)
app.config.from_object('auchapp.settings')

from auchapp import api