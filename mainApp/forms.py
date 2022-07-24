from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateTimeLocalField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from mainApp.models.user import User
from mainApp.models.status import Status


class RegisterForm(FlaskForm):
    role = [("admin", "admin"),
            ("user", "user")]

    def validate_username(self, username_to_check):
        user = User.query.filter(
            User.username == username_to_check.data).first()
        if user:
            raise ValidationError(
                'User already exist! please try a different username')

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
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
    username = StringField(label="User Name:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label='Sign in')


class StatusForm(FlaskForm):
    prod = [("Prod", "Prod"),
            ("Error", "Error")]

    def validate_statusName(self, statusName_to_check):
        status = Status.query.filter(
            Status.statusName == statusName_to_check.data).first()
        if status:
            raise ValidationError(
                'Status already exist! please try a different statusName')

    def validate_statusCode(self, statusCode_to_check):
        status = Status.query.filter(
            Status.statusCode == statusCode_to_check.data).first()
        if status:
            raise ValidationError(
                'Status already exist! please try a different statusCode')

    statusCode = IntegerField(label="Status Code:")
    statusName = StringField(label="Status Name:", validators=[DataRequired()])
    production = SelectField(label='Production Status:', choices=prod)
    submit = SubmitField(label='Add new status')


class ProductForm(FlaskForm):
    orderStatList = [("Open", "Open"),
                     ("Wait", "Wait"),
                     ("Close", "Close")]

    modelCode = StringField(label="Model Code:", validators=[DataRequired()])
    modelName = StringField(label="Model Name:", validators=[DataRequired()])
    orderStatus = SelectField(
        label='Production Status:', choices=orderStatList)
    startDate = DateTimeLocalField('startDate', validators=[DataRequired()],
                                   format='%Y-%m-%d %H:%M:%S')
    executionDate = DateTimeLocalField('executionDate', validators=[DataRequired()],
                                       format='%Y-%m-%d %H:%M:%S')
    submit = SubmitField(label='Add new product')
