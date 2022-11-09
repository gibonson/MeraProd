from flask_wtf import FlaskForm
from wtforms import SelectField, DateTimeLocalField, IntegerField, SubmitField
from wtforms.validators import DataRequired



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
