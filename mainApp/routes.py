from mainApp import app
from mainApp import db
from mainApp.models.user import User
from mainApp.models.product import Product
from mainApp.models.event import Event
from mainApp.models.status import Status
from flask import render_template, request, redirect, url_for, flash, send_file
from datetime import datetime, timedelta
from sqlalchemy import or_, and_
from flask_babel import gettext
import string
from mainApp.auth.auth import admin_check, login_required, user_table_page
from mainApp.auth.forms import RegisterForm, LoginForm
from mainApp.products.products import product_page, product_table_page, product_finished_table_page, active_product_page, product_summary_page
from mainApp.events.events import openEventsCounter
from mainApp.statuses.statuses import status_page
from mainApp.notification.emailSender import emailSender


@app.route('/')
@app.route('/home')
def home_page():
    openEvents = openEventsCounter()
    prodStart = gettext('Przykladowy teskt startowy')

    return render_template('home.html', prodStart=prodStart, openEvents=openEvents)


@app.route('/download')
@login_required
@admin_check
def download_report_page():
    path = "../output/raport.xls"
    try:
        return send_file(path, as_attachment=True)
    except:
        flash(f'File download error!', category='danger')
        return render_template('404.html')


@app.route('/emailSend')
@login_required
@admin_check
def email():
    emailSender()
    return "ok"

@ app.route('/help')
def help():
    return'help', 400


@ app.errorhandler(404)
def not_found(e):
    flash(f'404!', category='danger')
    return render_template('404.html')
