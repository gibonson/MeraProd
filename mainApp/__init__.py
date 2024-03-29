from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions import database_exists
from flask_login import LoginManager
from flask_babel import Babel, gettext

import os



# Init app
app = Flask(__name__, static_folder='../static')
baseDir = os.path.abspath(os.path.dirname(__file__))   + "//..//userFiles"
print(baseDir)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

# DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
#     os.path.join(baseDir, 'db.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(baseDir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init login
login_manager = LoginManager(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = "info"

if database_exists(app.config["SQLALCHEMY_DATABASE_URI"]):
    print('date base exist!')
else:
    print('no db')

# Init Babel
# app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel(app, default_locale="en")

@babel.localeselector
def get_locale():
    print('translate')
    return 'pl'

from mainApp import routes