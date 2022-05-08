from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from flask_marshmallow import Marshmallow 

# Init app
app = Flask(__name__)
baseDir = os.path.abspath(os.path.dirname(__file__))

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(baseDir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    belegNumber = db.Column(db.String(20), unique=True)
    modelName = db.Column(db.String(20))
    lenght = db.Column(db.Integer)
    numberOfParts = db.Column(db.Integer)
    bracket = db.Column(db.Boolean)
    singleOrDouble = db.Column(db.Integer)

    def __init__(self, belegNumber, modelName,lenght, numberOfParts, bracket, singleOrDouble):
        self.id = id
        self.belegNumber = belegNumber
        self.modelName = modelName
        self.lenght = lenght
        self.numberOfParts =numberOfParts
        self.bracket = bracket
        self.singleOrDouble = singleOrDouble


# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','belegNumber',   'modelName','lenght','numberOfParts','bracket','singleOrDouble')



# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)



print(baseDir)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/help')
def help():
    return'help'

@app.errorhandler(404)
def not_found(e):
    return '404'
