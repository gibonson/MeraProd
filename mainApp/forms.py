from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField, DateTimeLocalField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from mainApp.models.user import User
from mainApp.models.status import Status
from mainApp.models.product import Product
from flask_babel import gettext


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
                     ("Auto", "Auto"),
                     ("Close", "Close")]
    check_startDate = 0
    check_executionDate = 0

    def validate_modelCode(self, modelCode_to_check):
        product = Product.query.filter(
            Product.modelCode == modelCode_to_check.data).first()
        if product:
            raise ValidationError(
                'Product already exist! please try a different modelCode')

    def validate_startDate(self, startDate_to_check):
        self.check_startDate = startDate_to_check.data.timestamp()

    def validate_executionDate(self, executionDate_to_check):
        self.check_executionDate = executionDate_to_check.data.timestamp()
        difference = self.check_executionDate - self.check_startDate
        if difference <= 0:
            raise ValidationError(
                'Date error! please set a sorrect date')

    modelCode = StringField(label="Model Code:", validators=[
                            DataRequired(message='*Required')])
    modelName = StringField(label="Model Name:", validators=[
                            DataRequired(message='*Required')])
    orderStatus = SelectField(
        label='Production Status:', choices=orderStatList)
    startDate = DateTimeLocalField(label="Start Date:", validators=[DataRequired()],
                                   format='%Y-%m-%dT%H:%M')
    executionDate = DateTimeLocalField(label="Execution Date:", validators=[DataRequired()],
                                       format='%Y-%m-%dT%H:%M')
    submit = SubmitField(label='Add new product')


class EventForm(FlaskForm):
    activProductList = []
    idStatusList = []

    idProd = SelectField(
        label='Product Code:', validators=[DataRequired()], choices=activProductList)
    idStatus = SelectField(
        label='Status Name:', validators=[DataRequired()], choices=idStatusList)
    startDate = DateTimeLocalField(label="Start Date:", validators=[DataRequired()],
                                   format='%Y-%m-%dT%H:%M')
    endDate = DateTimeLocalField(label="Start Date:", validators=[DataRequired()],
                                 format='%Y-%m-%dT%H:%M')
    okCounter = IntegerField(label="Ok Counter:")
    nokCounter = IntegerField(label="Nok Counter:")
    userID = IntegerField(label="- ID:", validators=[
        DataRequired(message='*Required')])
    submit = SubmitField(label='Start Event')


class ProductOpenStatusForm(FlaskForm):
    submit = SubmitField(label="Set Open Status")


class ProductCloseStatusForm(FlaskForm):
    submit = SubmitField(label="Set Close Status")


class ProductAutoStatusForm(FlaskForm):
    submit = SubmitField(label="Set Auto Status")


class ProductEditForm(FlaskForm):
    submit = SubmitField(label="Set Edit Status")


# class EventStartForm(FlaskForm):
#     idProd = HiddenField(label='Product Code:', validators=[DataRequired()])
#     idStatus = HiddenField(label='Status Name:', validators=[DataRequired()])
#     startDate = DateTimeLocalField(label="Start Date:", validators=[DataRequired()],
#                                    format='%Y-%m-%dT%H:%M')
#     userID = IntegerField(label="- ID:", validators=[
#         DataRequired(message='*Required')])
#     submit = SubmitField(label='Start Event')

# class CloseAllEvents(FlaskForm):
#     submit  = SubmitField(label="Close all events")


class EventStartForm(FlaskForm):
    submit = SubmitField(label="Start Event")

class EventCloseForm(FlaskForm):
    okCounter = IntegerField(label="Ok Counter:", validators=[DataRequired()])
    nokCounter = IntegerField(label="Nok Counter:", validators=[DataRequired()])
    submit = SubmitField(label="Close Event")


class SetdateRange(FlaskForm):
    startDate = DateTimeLocalField(label="Start Date:", validators=[DataRequired()],
                                   format='%Y-%m-%dT%H:%M')
    endDate = DateTimeLocalField(label="End Date:", validators=[DataRequired()],
                                 format='%Y-%m-%dT%H:%M')
    submit = SubmitField(label='Set date range')


class ActiveProduct(FlaskForm):
    modelCode = StringField(label="Model Code:", validators=[
                            DataRequired(message='*Required')])
    submit = SubmitField(label='Active')