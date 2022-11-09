from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SelectField, SubmitField
from mainApp.models.status import Status
from wtforms.validators import ValidationError, DataRequired



class StatusForm(FlaskForm):
    prod = [("Prod", "Prod"),
            ("TPZ", "TPZ"),
            ("Error", "Error"),
            ("Finish", "Finish")]

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
