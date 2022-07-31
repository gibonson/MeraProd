from mainApp import app
from mainApp import db
from mainApp.forms import RegisterForm, LoginForm, StatusForm, ProductForm, EventForm
from mainApp.models.user import User
from mainApp.models.product import Product
from mainApp.models.event import Event
from mainApp.models.status import Status
from flask_login import login_required, logout_user, login_user
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta


@app.route('/')
@app.route('/home')
def home_page():
    referrer = request.referrer
    print(referrer)
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data, email_address=form.email_address.data, role=form.role.data)
        user_to_create.set_password(form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(
            f'Success! usser created: {user_to_create.username}', category='success')
        login_user(user_to_create)
        return redirect(url_for('home_page'))
    if form.errors != {}:  # validation errors
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('registerForm.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter(
            User.username == form.username.data).first()
        if attempted_user and attempted_user.check_password(form.password.data):
            login_user(attempted_user)
            flash(
                f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('home_page'))
        else:
            flash(f'User name or password incorrect!', category='danger')

    return render_template('loginForm.html', form=form)


@app.route('/logout')
@login_required
def logout_page():
    logout_user()
    flash(f'You have been logged out!', category='info')

    return redirect(url_for('home_page'))


@app.route('/status', methods=['GET', 'POST'])
@login_required
def status_page():
    form = StatusForm()
    if form.validate_on_submit():
        status_to_create = Status(
            form.statusCode.data, form.statusName.data, form.production.data)
        db.session.add(status_to_create)
        db.session.commit()
        flash(
            f'Success! status added: {status_to_create.statusName}', category='success')
        return redirect(url_for('home_page'))
    if form.errors != {}:  # validation errors
        for err_msg in form.errors.values():
            flash(f'Status incorrect!: {err_msg}', category='danger')

    return render_template('statusForm.html', form=form)


@app.route('/product', methods=['GET', 'POST'])
@login_required
def product_page():
    form = ProductForm()

    if form.validate_on_submit():
        product_to_create = Product(form.modelCode.data, form.modelName.data,
                                    form.orderStatus.data, int(form.startDate.data.timestamp()), int(form.executionDate.data.timestamp()))
        db.session.add(product_to_create)
        db.session.commit()
        flash(
            f'Success! product added: {product_to_create.modelCode}', category='success')
    if form.errors != {}:  # validation errors
        for err_msg in form.errors.values():
            flash(f'Product incorrect!: {err_msg}', category='danger')

    return render_template('productForm.html', form=form)


@app.route('/event', methods=['GET', 'POST'])
@login_required
def event_page():

    EventForm.activProductList.clear()
    EventForm.idStatusList.clear()
    activProductListDB = Product.query.filter(Product.orderStatus == 'Open')
    for row in activProductListDB:
        EventForm.activProductList.append(
            (row.id, str(row.modelCode) + " - " + row.modelName))
    idStatusListDB = Status.query.all()
    for row in idStatusListDB:
        EventForm.idStatusList.append(
            (row.id, str(row.statusCode) + " - " + row.statusName))
    form = EventForm()

    if form.validate_on_submit():
        print(form.idProd.data)
        print(form.idStatus.data)
        startDate = form.startDate.data
        print(startDate.timestamp())
        endDate = form.endDate.data
        print(endDate.timestamp())
        print(form.okCounter.data)
        print(form.nokCounter.data)
        print(form.userID.data)
        event_to_create = Event(int(form.idProd.data), int(form.idStatus.data), int(form.startDate.data.timestamp()), int(
            form.endDate.data.timestamp()), form.okCounter.data, form.nokCounter.data, int(form.userID.data))
        db.session.add(event_to_create)
        db.session.commit()
        flash(
            f'Success! event added: {event_to_create}', category='success')
    if form.errors != {}:  # validation errors
        for err_msg in form.errors.values():
            flash(f'Product incorrect!: {err_msg}', category='danger')

    return render_template('eventForm.html', form=form)

@app.route('/producttable', methods=['GET', 'POST'])
@login_required
def product_table_page():
    products = Product.query.all()
    for product in products:
        product.delta= round((product.executionDate - product.startDate)/86400,1)
        product.startDate = datetime.fromtimestamp(product.startDate)
        product.executionDate = datetime.fromtimestamp(product.executionDate)
    return render_template('productTable.html', products=products)


# granica poprawności:D
# granica poprawności:D
# granica poprawności:D
# granica poprawności:D
# granica poprawności:D
# granica poprawności:D
# granica poprawności:D


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
