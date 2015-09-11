import os

from flask import Flask

app = Flask(__name__)

cfg = os.getenv('CONFIG', 'Production')
app.config.from_object('auchapp.settings.%sConfig' % cfg)

from auchapp import api