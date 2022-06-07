from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, request
from wtforms import Form, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import datetime

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
    orderStatus = db.Column(db.Integer)
    executionDate = db.Column(db.DateTime)

    def __init__(self, belegNumber, modelName, lenght, numberOfParts, bracket, singleOrDouble, orderStatus, executionDate):
        self.belegNumber = belegNumber
        self.modelName = modelName
        self.lenght = lenght
        self.numberOfParts = numberOfParts
        self.bracket = bracket
        self.singleOrDouble = singleOrDouble
        self.orderStatus = orderStatus
        self.executionDate = executionDate

# Product Schema


class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'belegNumber', 'modelName', 'lenght',
                  'numberOfParts', 'bracket', 'singleOrDouble', 'orderStatus', 'executionDate')


# Init schema
product_schema = ProductSchema()
#products_schema = ProductSchema(strict=True, many=True)
products_schema = ProductSchema(many=True)


# EventType Class/Model
class EventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idEvent = db.Column(db.Integer)
    eventName = db.Column(db.String(20), unique=True)

    def __init__(self, idEvent, eventName):
        self.idEvent = idEvent
        self.eventName = eventName


# EventType Schema
class EventTypeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'idEvent', 'eventName')


# Init schema
EventType_schema = EventTypeSchema()
#products_schema = EventTypeSchema(strict=True, many=True)
EventType_schema = EventTypeSchema(many=True)


# Status Class/Model
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProd = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=True)
    idEvent = db.Column(db.Integer)
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    okCounter = db.Column(db.Integer)
    nokCounter = db.Column(db.Integer)

    def __init__(self, idProd, idEvent, startDate, endDate, okCounter, nokCounter):
        self.idProd = idProd
        self.idEvent = idEvent
        self.startDate = startDate
        self.endDate = endDate
        self.okCounter = okCounter
        self.nokCounter = nokCounter

# Status Schema


class StatusSchema(ma.Schema):
    class Meta:
        fields = ('id', 'idProd', 'idEvent', 'startDate',
                  'endDate', 'okCounter', 'nokCounter')


# Init schema
status_schema = StatusSchema()
statuses_schema = StatusSchema(many=True)


# API Create a Product
@app.route('/product', methods=['POST'])
def addProduct():
    belegNumber = request.json['belegNumber']
    modelName = request.json['modelName']
    lenght = request.json['lenght']
    numberOfParts = request.json['numberOfParts']
    bracket = request.json['bracket']
    singleOrDouble = request.json['singleOrDouble']
    orderStatus = request.json['orderStatus']
    executionDate = request.json['executionDate']

    newProduct = Product(belegNumber, modelName, lenght,
                         numberOfParts, bracket, singleOrDouble, orderStatus, executionDate)
    db.session.add(newProduct)
    db.session.commit()

    return product_schema.jsonify(newProduct)


# API Get All Products
@app.route('/product', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)


# API Get Product
@app.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)


# API Update a Product
@app.route('/product/<id>', methods=['PUT'])
def updateProduct(id):

    product = Product.query.get(id)

    belegNumber = request.json['belegNumber']
    modelName = request.json['modelName']
    lenght = request.json['lenght']
    numberOfParts = request.json['numberOfParts']
    bracket = request.json['bracket']
    singleOrDouble = request.json['singleOrDouble']
    orderStatus = request.json['orderStatus']
    executionDate = request.json['executionDate']

    product.belegNumber = belegNumber
    product.modelName = modelName
    product.lenght = lenght
    product.numberOfParts = numberOfParts
    product.bracket = bracket
    product.singleOrDouble = singleOrDouble
    product.orderStatus = orderStatus
    product.executionDate = executionDate

    db.session.commit()

    return product_schema.jsonify(product)


# API Delete Product
@app.route('/product/<id>', methods=['DELETE'])
def del_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)


# GUI
@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/getTable')
def getTable():
    all_products = Product.query.all()
    all_Statuses = Status.query.all()
    eventList = EventType.query.all()
    for column in all_products:
        print("% s % s" % (column.id, column.lenght))
        for status in all_Statuses:
            if column.id is status.idProd:
                print(status.startDate)

    return render_template('table.html', all_products=all_products, all_Statuses=all_Statuses, eventList=eventList)


@app.route('/getTable2')
def getTable2():
    all_products = Product.query.filter(Product.orderStatus == 1)
    for column in all_products:
        print("% s % s" % (column.id, column.lenght))
    return render_template('table.html', all_products=all_products)


@app.route('/removeProduct', methods=['GET', 'POST'])
def removeProduct():
    if request.method == 'POST':
        id = request.form['id']
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('getTable'))


@app.route('/setFinishProduct', methods=['GET', 'POST'])
def setFinishProduct():
    if request.method == 'POST':
        id = request.form['id']
        product = Product.query.get(id)
        product.orderStatus = 2
        db.session.commit()

    return redirect(url_for('getTable'))


@app.route('/setActivProduct', methods=['GET', 'POST'])
def setActivProduct():
    if request.method == 'POST':

        activList = Product.query.filter(Product.orderStatus == 1)
        for column in activList:
            column.orderStatus = 2
            db.session.commit()
        id = request.form['id']
        product = Product.query.get(id)
        product.orderStatus = 1
        db.session.commit()

    return redirect(url_for('getTable'))


messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]


@app.route('/create', methods=('GET', 'POST'))
def create():
    messages.clear()
    today = datetime.date.today()
    today = today.strftime('%Y-%m-%d')
    print(today)

    if request.method == 'POST':
        belegNumber = request.form['belegNumber']
        modelName = request.form['modelName']
        lenght = request.form['lenght']
        numberOfParts = request.form['numberOfParts']
        bracket = request.form['bracket']
        if bracket == "True":
            bracket = True
        if bracket == "False":
            bracket = False
        singleOrDouble = request.form['singleOrDouble']
        orderStatus = request.form['orderStatus']
        executionDate = request.form['executionDate']
        format = "%Y-%m-%d"
        executionDate = datetime.datetime.strptime(executionDate, format)

        if not belegNumber:
            flash('belegNumber is required!')
        elif not modelName:
            flash('modelName is required!')
        else:
            # flash(title + " " + content + " added")
            messages.append({'title': belegNumber, 'content': modelName})
            # # return redirect(url_for('getTable'))
            # # return redirect(url_for('getTable'))
            newProduct = Product(belegNumber, modelName, lenght, numberOfParts,
                                 bracket, singleOrDouble, orderStatus, executionDate)
            db.session.add(newProduct)
            db.session.commit()

            return render_template('createForm.html', messages=messages, today=today)

    return render_template('createForm.html', messages=messages, today=today)


@app.route('/setStatus', methods=('GET', 'POST'))
def setStatus():
    messages.clear()
    today = datetime.datetime.today()
    print(today)

    activProductList = Product.query.filter(Product.orderStatus == 1)
    for column in activProductList:
        print("% s % s" % (column.id, column.lenght))
    eventList = EventType.query.all()
    openStatuses = Status.query.filter(Status.endDate == None)

    if request.method == 'POST':
        idProd = request.form['idProd']
        idEvent = request.form['idEvent']

        if not idProd:
            flash('idProd is required!')
        elif not idEvent:
            flash('idEvent is required!')
        else:
            messages.append({'title': idProd, 'content': idEvent + "added"})
            newStatus = Status(idProd, idEvent, startDate=today,
                               endDate=None, okCounter=None, nokCounter=None)

            emptyEndDateList = Status.query.filter(Status.endDate == None)
            for column in emptyEndDateList:
                column.endDate = today

            db.session.add(newStatus)
            db.session.commit()

            return render_template('setStatusForm.html', messages=messages, today=today, activProductList=activProductList, eventList=eventList, openStatuses=openStatuses)

    return render_template('setStatusForm.html', messages=messages, today=today, activProductList=activProductList, eventList=eventList, openStatuses=openStatuses)


@app.route("/closeAllStatuses", methods=('GET', 'POST'))
def closeAllStatuses():
    messages.clear()
    today = datetime.datetime.today()
    print(today)
    emptyEndDateList = Status.query.filter(Status.endDate == None)
    for column in emptyEndDateList:
        column.endDate = today

    db.session.commit()
    return redirect((url_for('setStatus')))


@app.route('/help')
def help():
    return'help', 400


@app.errorhandler(404)
def not_found(e):
    return '404'


print(baseDir)
