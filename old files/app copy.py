from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, request
from wtforms import Form, TextAreaField, validators, StringField, SubmitField
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, current_user, login_required, login_user, logout_user
import os
from datetime import datetime, timedelta
import time


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
login = LoginManager()
login.login_view = 'login'
login.init_app(app)


messages = [{'title': 'Message One',
             'content': 'Message One Content'},
            {'title': 'Message Two',
             'content': 'Message Two Content'}
            ]

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

# EventType Class/Model


class EventType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idEvent = db.Column(db.Integer)
    eventName = db.Column(db.String(20), unique=True)

    def __init__(self, idEvent, eventName):
        self.idEvent = idEvent
        self.eventName = eventName


# Users Class/Model
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())
    role = db.Column(db.Integer)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Status Class/Model


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProd = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=True)
    idEvent = db.Column(db.Integer)
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    okCounter = db.Column(db.Integer)
    nokCounter = db.Column(db.Integer)
    userID = db.Column(db.Integer, db.ForeignKey(Users.id))

    def __init__(self, idProd, idEvent, startDate, endDate, okCounter, nokCounter, userID):
        self.idProd = idProd
        self.idEvent = idEvent
        self.startDate = startDate
        self.endDate = endDate
        self.okCounter = okCounter
        self.nokCounter = nokCounter
        self.userID = userID

    def sub(self, endDate, startDate):
        return(endDate - startDate)


@login.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/addUser', methods=['GET', 'POST'])
@login_required
def addUser():
    messages.clear()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if Users.query.filter(Users.username == username).first():
            flash('username already Present')
        elif not username:
            flash('username is required!')
        elif not password:
            flash('password is required!')
        else:
            messages.append({'title': username, 'content': password})
            user = Users(username=username, role=role)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return render_template('addUser.html', messages=messages)

    return render_template('addUser.html', messages=messages)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter(Users.username == username).first()
        if user is None:
            return "bad user"
        if password is None:
            return "bad password"
        elif user.check_password(password):
            login_user(user)
            return redirect(url_for('getTable'))
        else:
            return "bad pass"
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/showUser')
@login_required
def showUser():
    print(current_user.username)
    return 'curetn user is ' + current_user.username

# GUI


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/getTable')
@login_required
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


@app.route('/getTimeRange/<delta>')
@ login_required
def getTimeRange(delta):
    delta = int(delta)
    dateToday = datetime.today()
    day = dateToday - timedelta(delta)+timedelta(1)
    dateRangeMax = datetime(
        day.year, day.month, day.day, 6, 0, 0, 0)
    dateRangeMin = dateRangeMax - timedelta(days=1)

    results = db.session.query(Status, Users, Product, EventType).filter(
        Status.startDate >= dateRangeMin, Status.startDate <= dateRangeMax, Status.userID == Users.id, Status.idProd == Product.id, EventType.idEvent == Status.idEvent)
    for status, users, product, event in results:
        print(status.userID, users.username,
              status.endDate - status.startDate, status.id, product.belegNumber, event.eventName)

    # statusesByDay = Status.query.filter(
    #     Status.startDate >= dateRangeMin, Status.startDate <= dateRangeMax).join(Users.id)

    # for statusByDay in statusesByDay:
    #     print(statusByDay)
    #     # final = str(statusByDay) + " -> " + str(statusByDay.startDate) + " -> " + str(statusByDay.endDate) + " "+ str(statusByDay.users.username)
    #     # print(final)
    delta = int(delta)
    dateRangeMax = str(dateRangeMax)
    dateRangeMin = str(dateRangeMin)

    resultsSum = db.session.query(Status.idEvent,  EventType.eventName, db.func.count(Status.idEvent)).filter(
        Status.startDate >= dateRangeMin, Status.startDate <= dateRangeMax, Status.userID == Users.id, Status.idProd == Product.id, EventType.idEvent == Status.idEvent).outerjoin(Status, Status.idEvent == EventType.idEvent).group_by(EventType.eventName).all()
    for res in resultsSum:
        print(res)



    print()

    return render_template('getTimeRange.html', results=results, delta=delta, dateRangeMax=dateRangeMax, dateRangeMin=dateRangeMin)


@ app.route('/removeProduct', methods=['GET', 'POST'])
def removeProduct():
    if request.method == 'POST':
        id = request.form['id']
        product = Product.query.get(id)
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('getTable'))


@ app.route('/setFinishProduct', methods=['GET', 'POST'])
def setFinishProduct():
    if request.method == 'POST':
        id = request.form['id']
        product = Product.query.get(id)
        product.orderStatus = 2
        db.session.commit()

    return redirect(url_for('getTable'))


@ app.route('/setActivProduct', methods=['GET', 'POST'])
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


@ app.route('/create', methods=('GET', 'POST'))
@ login_required
def create():
    messages.clear()
    today = datetime.today()
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


@ app.route('/setStatus', methods=('GET', 'POST'))
@ login_required
def setStatus():
    messages.clear()
    today = datetime.today()
    print(today)
    activProductList = Product.query.filter(Product.orderStatus == 1)
    for column in activProductList:
        print("% s % s" % (column.id, column.lenght))
    eventList = EventType.query.all()
    openStatuses = Status.query.filter(Status.endDate == None)

    if request.method == 'POST':
        idProd = request.form['idProd']
        idEvent = request.form['idEvent']
        userID = request.form['userID']

        if not idProd:
            flash('idProd is required!')
        elif not idEvent:
            flash('idEvent is required!')
        elif not userID:
            flash('userID is required!')
        else:
            messages.append({'title': idProd, 'content': idEvent})
            newStatus = Status(idProd, idEvent, startDate=today,
                               endDate=None, okCounter=None, nokCounter=None, userID=userID)

            emptyEndDateList = Status.query.filter(Status.endDate == None)
            for column in emptyEndDateList:
                column.endDate = today

            db.session.add(newStatus)
            db.session.commit()

            return render_template('setStatusForm.html', messages=messages, today=today, activProductList=activProductList, eventList=eventList, openStatuses=openStatuses)

    return render_template('setStatusForm.html', messages=messages, today=today, activProductList=activProductList, eventList=eventList, openStatuses=openStatuses)


@ app.route("/closeAllStatuses", methods=('GET', 'POST'))
def closeAllStatuses():
    messages.clear()
    today = datetime.today()
    print(today)
    emptyEndDateList = Status.query.filter(Status.endDate == None)
    for column in emptyEndDateList:
        column.endDate = today

    db.session.commit()
    return redirect((url_for('setStatus')))


@ app.route('/help')
def help():
    return'help', 400


@ app.errorhandler(404)
def not_found(e):
    return '404'


print(baseDir)
