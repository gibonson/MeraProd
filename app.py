from flask import Flask, render_template, request, jsonify ,redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os



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
        self.belegNumber = belegNumber
        self.modelName = modelName
        self.lenght = lenght
        self.numberOfParts =numberOfParts
        self.bracket = bracket
        self.singleOrDouble = singleOrDouble


# Product Schema
class ProductSchema(ma.Schema):
  class Meta:
        fields = ('id','belegNumber','modelName','lenght','numberOfParts','bracket','singleOrDouble')



# Init schema
product_schema = ProductSchema()
#products_schema = ProductSchema(strict=True, many=True)
products_schema = ProductSchema(many=True)




#API Create a Product
@app.route('/product', methods = ['POST'])
def addProduct():
    belegNumber = request.json['belegNumber']
    modelName = request.json['modelName']
    lenght = request.json['lenght']
    numberOfParts = request.json['numberOfParts']
    bracket = request.json['bracket']
    singleOrDouble = request.json['singleOrDouble']

    newProduct = Product(belegNumber, modelName, lenght, numberOfParts, bracket, singleOrDouble)
    db.session.add(newProduct)
    db.session.commit()

    return product_schema.jsonify(newProduct)


#API Get All Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


#API Get Product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


#API Update a Product
@app.route('/product/<id>', methods = ['PUT'])
def updateProduct(id):

    product = Product.query.get(id)

    belegNumber = request.json['belegNumber']
    modelName = request.json['modelName']
    lenght = request.json['lenght']
    numberOfParts = request.json['numberOfParts']
    bracket = request.json['bracket']
    singleOrDouble = request.json['singleOrDouble']

    product.belegNumber = belegNumber
    product.modelName = modelName
    product.lenght = lenght
    product.numberOfParts = numberOfParts
    product.bracket = bracket
    product.singleOrDouble = singleOrDouble


    db.session.commit()

    return product_schema.jsonify(product)


#GUI
@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/help')
def help():
    return'help'


@app.errorhandler(404)
def not_found(e):
    return '404'


print(baseDir)