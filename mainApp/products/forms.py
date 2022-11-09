from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateTimeLocalField, SubmitField
from wtforms.validators import ValidationError, DataRequired
from mainApp.models.product import Product

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


class ProductOpenStatusForm(FlaskForm):
    submit = SubmitField(label="Set Open Status")


class ProductCloseStatusForm(FlaskForm):
    submit = SubmitField(label="Set Close Status")


class ProductAutoStatusForm(FlaskForm):
    submit = SubmitField(label="Set Auto Status")


class ProductEditForm(FlaskForm):
    submit = SubmitField(label="Set Edit Status")


class ActiveProduct(FlaskForm):
    modelCode = StringField(label="Model Code:", validators=[
                            DataRequired(message='*Required')])
    submit = SubmitField(label='Active')
