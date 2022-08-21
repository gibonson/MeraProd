from mainApp import app
from mainApp import db
from mainApp.forms import RegisterForm, LoginForm, StatusForm, ProductForm, EventForm, ProductOpenStatusForm, ProductCloseStatusForm, ProductWaitStatusForm, ProductEditForm, EventStartForm, EventCloseForm
from mainApp.models.user import User
from mainApp.models.product import Product
from mainApp.models.event import Event
from mainApp.models.status import Status
from flask_login import login_required, logout_user, login_user
from flask import render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from openpyxl import Workbook
import string

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
        startDate = form.startDate.data
        endDate = form.endDate.data
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


@ app.route('/eventStartStop', methods=('GET', 'POST'))
@ login_required
def event_start_stop_page():
    eventStartForm = EventStartForm()
    eventCloseForm = EventCloseForm()
    if request.method == 'POST':
        if request.form['idEvent'] != "None":
            okCounter = request.form['okCounter']
            nokCounter = request.form['nokCounter']
            eventID = request.form['idEvent']
            event_to_close = Event.query.get(eventID)

            now = datetime.today()
            now = now.timestamp()
            now = int(now)
            event_to_close.okCounter = okCounter
            event_to_close.nokCounter = nokCounter
            event_to_close.endDate = now

            db.session.add(event_to_close)
            db.session.commit()
            flash(
                f'Success! Event closed: {eventID}', category='success')
        else:
            idProd = request.form['idProd']
            print(idProd)
            idStatus = request.form['idStatus']
            print(idStatus)
            idUser = request.form['idUser']
            print(idUser)
            today = datetime.today()
            today = today.timestamp()
            today = int(today)
            print(today)
            event_to_create = Event(idProd=idProd, idStatus=idStatus, startDate=today, endDate=None, nokCounter=None,
                                    okCounter=None,  userID=idUser)
            db.session.add(event_to_create)
            db.session.commit()
            flash(
                f'Success! Event Start: {idProd} - {idStatus}', category='success')
    openProductList = Product.query.filter(Product.orderStatus == "Open")
    statusList = Status.query.all()
    openEventList = Event.query.filter(Event.endDate == None)

    return render_template('eventStartForm.html', openProductList=openProductList, statusList=statusList, openEventList=openEventList, eventStartForm=eventStartForm, eventCloseForm=eventCloseForm)


@ app.route('/eventAllStop', methods=('GET', 'POST'))
@ login_required
def event_all_stop_page():
    now = datetime.today()
    now = now.timestamp()
    now = int(now)
    activEventList = Event.query.filter(Event.endDate == None)
    for column in activEventList:
        print(column.id)
        column.endDate = now
    db.session.commit()

    return redirect((url_for('event_start_stop_page')))


@app.route('/productTable', methods=['GET', 'POST'])
@login_required
def product_table_page():
    productCloseStatusForm = ProductCloseStatusForm()
    productOpenStatusForm = ProductOpenStatusForm()
    productWaitStatusForm = ProductWaitStatusForm()
    productEditForm = ProductEditForm()
    if request.method == 'POST':
        productID = request.form.get('productID')
        newStatus = request.form.get('newStatus')
        if newStatus == "Edit":
            modelCode = request.form.get('modelCode')
            modelName = request.form.get('modelName')
            orderStatus = request.form.get('orderStatus')
            startDate = request.form.get('startDate')
            executionDate = request.form.get('executionDate')
            startDateDate = datetime.strptime(startDate, "%Y-%m-%dT%H:%M")
            executionDateDate = datetime.strptime(
                executionDate, "%Y-%m-%dT%H:%M")
            startDateDate = startDateDate.timestamp()
            executionDateDate = executionDateDate.timestamp()
            product = Product.query.get(productID)
            oldName = product.modelName
            product.modelCode = modelCode
            product.modelName = modelName
            product.orderStatus = orderStatus
            product.startDate = startDateDate
            product.executionDate = executionDateDate
            db.session.commit()
            flash(
                f"Edited product from {oldName} to {modelName}", category='success')
        else:
            product = Product.query.get(productID)
            oldStatus = product.orderStatus
            product.orderStatus = newStatus
            db.session.commit()
            flash(
                f"Changed product status from {oldStatus} to {newStatus}", category='success')

    products = Product.query.all()
    for product in products:
        product.delta = round(
            (product.executionDate - product.startDate)/86400, 1)
        product.startDate = datetime.fromtimestamp(product.startDate)
        product.executionDate = datetime.fromtimestamp(product.executionDate)
    return render_template('productTable.html', products=products, productOpenStatusForm=productOpenStatusForm, productCloseStatusForm=productCloseStatusForm, productWaitStatusForm=productWaitStatusForm, productEditForm=productEditForm)


@app.route('/eventTable', methods=['GET', 'POST'])
@login_required
def event_table_page():
    results = db.session.query(Status, User, Product, Event).filter(
        Event.startDate, Event.startDate, Event.userID == User.id, Event.idProd == Product.id, Event.idStatus == Status.id)

    finalEventTable = []
    for status, user, product, event in results:
        finalEvent = {}
        finalEvent["id"] = event.id
        finalEvent["modelCode"] = product.modelCode
        finalEvent["modelName"] = product.modelName
        finalEvent["username"] = user.username
        finalEvent["statusName"] = status.statusName
        finalEvent["okCounter"] = event.okCounter
        finalEvent["nokCounter"] = event.nokCounter
        finalEvent["startDate"] = datetime.fromtimestamp(event.startDate)
        if event.endDate:
            finalEvent["endDate"] = datetime.fromtimestamp(event.endDate)
            finalEvent["delta"] = round(
                (event.endDate - event.startDate)/3600, 1)
        else:
            finalEvent["endDate"] = "in progress"
            finalEvent["delta"] = "in progress"
        finalEventTable.append(finalEvent)

    for resfinalEvent in finalEventTable:
        print(resfinalEvent)

    wb = Workbook()
    ws = wb.active
    ws1 = wb.create_sheet("test")
    ws.title = "New Title"
    ws.sheet_properties.tabColor = "1072BA"
    ws['A1'] = "id"
    ws['B1'] = "modelCode"
    ws['C1'] = "modelName"
    ws['D1'] = "username"
    ws['E1'] = "statusName"
    ws['F1'] = "okCounter"
    ws['G1'] = "nokCounter"
    ws['H1'] = "startDate"
    ws['I1'] = "endDate"
    ws['J1'] = "delta[h]"

    date_now = datetime.now()
    alphabet = list(string.ascii_lowercase)
    print(alphabet)
    row_counter = 1
    for resfinalEvent in finalEventTable:
        row_counter+=1
        ws['A'+str(row_counter)] = resfinalEvent["id"]
        ws['B'+str(row_counter)] = resfinalEvent["modelCode"]
        ws['C'+str(row_counter)] = resfinalEvent["modelName"]
        ws['D'+str(row_counter)] = resfinalEvent["username"]
        ws['E'+str(row_counter)] = resfinalEvent["statusName"]
        ws['F'+str(row_counter)] = resfinalEvent["okCounter"]
        ws['G'+str(row_counter)] = resfinalEvent["nokCounter"]
        ws['H'+str(row_counter)] = resfinalEvent["startDate"]
        ws['I'+str(row_counter)] = resfinalEvent["endDate"]
        ws['J'+str(row_counter)] = resfinalEvent["delta"]
        print(row_counter)
    output_file_name = "output/raport - " + str(date_now) + ".xls"
    wb.save(output_file_name)
    flash(f"Export complete! File name: {output_file_name}", category='success')

    

    return render_template('eventTable.html', finalEventTable=finalEventTable)


@app.route('/exportExcel', methods=['GET', 'POST'])
@login_required
def exportExcel():
    wb = Workbook()
    ws = wb.active
    ws1 = wb.create_sheet("test")
    ws.title = "New Title"
    ws.sheet_properties.tabColor = "1072BA"
    for x in range(1, 10):
        cell = 'A' + str(x)
        ws[cell] = x
    wb.save("testfile.xlsx")
    return "ok"


# granica poprawności:D
# granica poprawności:D
# granica poprawności:D
# granica poprawności:D
# granica poprawności:D
# granica poprawności:D
# granica poprawności:D


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


@ app.route('/help')
def help():
    return'help', 400


@ app.errorhandler(404)
def not_found(e):
    return '404'
