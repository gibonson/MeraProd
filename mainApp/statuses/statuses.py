from mainApp import app
from mainApp import db
from mainApp.models.status import Status
from mainApp.routes import render_template, flash, redirect, url_for
from mainApp.auth.auth import admin_check, login_required
from mainApp.events.events import openEventsCounter
from mainApp.statuses.forms import StatusForm


@app.route('/status', methods=['GET', 'POST'])
@login_required
@admin_check
def status_page():
    openEvents = openEventsCounter()
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

    return render_template('statusForm.html', form=form, openEvents=openEvents)
