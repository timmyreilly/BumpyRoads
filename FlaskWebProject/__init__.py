"""
The flask application package.
"""

from flask import Flask
from flask.ext.bootstrap import Bootstrap 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
bootstrap = Bootstrap(app)

import FlaskWebProject.views