from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Init app
app = Flask(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(baseDir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

print(baseDir)
from mainApp import routes