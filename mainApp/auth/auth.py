from mainApp import db
from mainApp import app
from mainApp.routes import redirect, url_for, render_template, flash
from mainApp.models.user import User
from mainApp.auth.forms import LoginForm, RegisterForm, ChangePassword
from functools import wraps
from flask_login import login_required, logout_user, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash


def admin_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.is_anonymous:
            return redirect(url_for('login_page'))
        elif current_user.role == "admin":
            print("you are admin")
        else:
            flash(f'You are not admin!', category='danger')
            return render_template('404.html')
        return func(*args, **kwargs)
    return wrapper


@app.route('/register', methods=['GET', 'POST'])
@login_required
@admin_check
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(
            username=form.username.data, email_address=form.email_address.data, role=form.role.data, active = "Y")
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

    LoginForm.userNameList.clear()
    user = User.query.filter(User.active == 'Y')
    print(user)
    for row in user:
        print(row.username)
        LoginForm.userNameList.append([row.username, row.username])

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


@app.route('/userTable', methods=['GET', 'POST'])
@login_required
@admin_check
def user_table_page():
    form = ChangePassword()
    if form.validate_on_submit():
        print("walidacja ok")
        print(form.userID.data)
        print(form.password1.data)
        user = User.query.get(form.userID.data)
        user.set_password(form.password1.data)
        db.session.commit()

    if form.errors != {}:  # validation errors
        for err_msg in form.errors.values():
            flash(
                f'There was an error with creating a user: {err_msg}', category='danger')

    users = User.query.all()
    return render_template('userTable.html', users=users, form=form)
