from mainApp import app
from mainApp import db
from mainApp.models.product import Product
from mainApp.models.status import Status
from mainApp.models.event import Event
from mainApp.routes import render_template, flash, request, datetime, redirect,url_for
from mainApp.auth.auth import admin_check, login_required
from mainApp.products.forms import ProductForm, ProductCloseStatusForm, ProductAutoStatusForm, ProductOpenStatusForm, ProductEditForm
from mainApp.notification.forms import EmailForm
from mainApp.notification.emailSender import emailSender
from mainApp.events.events import openEventsCounter
from sqlalchemy import or_, and_, func
import matplotlib.pyplot as plt
import re



@app.route('/product', methods=['GET', 'POST'])
@login_required
@admin_check
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
    openEvents = openEventsCounter()
    return render_template('productForm.html', form=form, openEvents=openEvents)


@app.route('/productTable', methods=['GET', 'POST'])
@login_required
def product_table_page():
    productCloseStatusForm = ProductCloseStatusForm()
    productOpenStatusForm = ProductOpenStatusForm()
    productAutoStatusForm = ProductAutoStatusForm()
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

    # products = Product.query.filter(Product.orderStatus == 'Finished')
    products = Product.query.all()
    for product in products:
        product.delta = "update"
        if product.startDate:
            product.delta = round(
                (product.executionDate - product.startDate)/86400, 1)
            product.startDate = datetime.fromtimestamp(product.startDate)
            product.executionDate = datetime.fromtimestamp(
                product.executionDate)
        else:
            product.delta = "update"
    openEvents = openEventsCounter()
    return render_template('productTable.html', products=products, productOpenStatusForm=productOpenStatusForm, productCloseStatusForm=productCloseStatusForm, productAutoStatusForm=productAutoStatusForm, productEditForm=productEditForm, openEvents=openEvents)


@app.route('/productFinishedTable', methods=['GET', 'POST'])
@login_required
def product_finished_table_page():
    form = EmailForm()

    if form.validate_on_submit():
            subject = form.contactReason.data + ": " + form.id.data
            message = form.message.data
            emailSender(subject = subject , message = message)


    products = Product.query.filter(Product.orderStatus == 'Finished').order_by(Product.id.desc())
    for product in products:
        if product.startDate:
            product.startDate = datetime.fromtimestamp(product.startDate)
            product.executionDate = datetime.fromtimestamp(
                product.executionDate)

    openEvents = openEventsCounter()
    return render_template('productFinishedTable.html', products=products, openEvents=openEvents, form = form)


@app.route('/activeProduct', methods=['GET', 'POST'])
@login_required
def active_product_page():
    productExist = False
    if request.method == 'POST':
        modelCode = request.form.get('modelCode')
        print(modelCode)
        products = Product.query.all()
        for product in products:
            if product.orderStatus != "Finished" or product.orderStatus != "Auto":
                product.orderStatus = "Close"
            if product.modelCode == modelCode:
                product.orderStatus = "Open"
                productExist = True
        db.session.commit()

        if not productExist:

            modelCodeRegexp = re.search(
                "[0-9]{4}\/[0-9]{2}\/[0-9]{2}\/ZP\/[0-9]+", modelCode)
            if not modelCodeRegexp:
                flash(
                    f'nameCode validation error: {modelCode}', category='danger')
                return redirect((url_for('event_start_stop_page')))

            product_to_create = Product(modelCode, "added by operator",
                                        "Open", None, None)
            db.session.add(product_to_create)
            db.session.commit()
            flash(
                f'Success! product added by operator: {product_to_create.modelCode}', category='success')

    return redirect((url_for('event_start_stop_page')))


@app.route('/productSummary', methods=['GET', 'POST'])
@login_required
def product_summary_page():
    if request.method == 'POST':
        idProd = request.form.get('productID')

        # modelCode = request.form.get('modelCode')
        results = db.session.query(Status, Event).with_entities(Event.id, Event.idStatus,  func.sum(Event.startDate).label("startDate"),  func.sum(Event.endDate).label("endDate"), func.sum(
            Event.endDate - Event.startDate).label("delta"), func.sum(Event.okCounter).label("okCounter"),  func.sum(Event.nokCounter).label("nokCounter"), Status.statusName, Status.production).filter(Event.idProd == idProd, Event.idStatus == Status.id).group_by(Event.idStatus).all()
        statuses = Status.query.all()
        # evetns = Event.query.filter(Event.idProd == idProd)

        finalResultsTable = []
        for result in results:
            finalEvent = {}

            finalEvent["idStatus"] = result.idStatus
            finalEvent["statusName"] = result.statusName
            finalEvent["production"] = result.production
            finalEvent["okCounter"] = result.okCounter
            finalEvent["nokCounter"] = result.nokCounter
            if result.endDate:
                finalEvent["delta"] = round(
                    (result.endDate - result.startDate)/3600, 3)
            else:
                finalEvent["delta"] = "in progress"
            finalResultsTable.append(finalEvent)

        plt.figure(figsize=(8, 5))
        values = []
        labels = []

        for finalResultTable in finalResultsTable:

            labels.append(finalResultTable["statusName"])
            values.append(finalResultTable["delta"])

        plt.pie(values, labels=labels, autopct='%.2f %%')
        plt.title('Summary Chart')
        plt.savefig('mainApp/static/new_plot.png')
        openEvents = openEventsCounter()

    return render_template('productSummaryTable.html', finalResultsTable=finalResultsTable, openEvents=openEvents)
