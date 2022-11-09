from flask_wtf import FlaskForm
from mainApp import gettext
from wtforms import StringField, PasswordField, SelectField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from mainApp.models.user import User


class RegisterForm(FlaskForm):
    role = [("admin", "admin"),
            ("user", "user")]

    def validate_username(self, username_to_check):
        user = User.query.filter(
            User.username == username_to_check.data).first()
        if user:
            raise ValidationError(
                gettext('User already exist! please try a different username'))

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter(
            User.email_address == email_address_to_check.data).first()
        if email_address:
            raise ValidationError(
                'Email already exist! please try a different email')

    username = StringField(label='User Name:', validators=[
                           Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(
        label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    role = SelectField(label='User role:', choices=role)
    submit = SubmitField(label=gettext('Create Account'))


class LoginForm(FlaskForm):
    username = StringField(label="User Name:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class ChangePassword(FlaskForm):
    userID = HiddenField(label='userID:')
    password1 = PasswordField(label='Password:', validators=[
                              Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[
                              EqualTo('password1'), DataRequired()])
    submit = SubmitField(label=gettext('Submit'))
