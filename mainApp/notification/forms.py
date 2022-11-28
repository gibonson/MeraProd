from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField,TextAreaField

class EmailForm(FlaskForm):
    contactReasonList = [("tory były złe", "tory były złe"),
                     ("pociąg też był zły", "pociąg też był zły"),
                     ("to zła kobieta była", "to zła kobieta była")]

    id = StringField(label="Model Code:")

    contactReason = SelectField(
        label='contactReason:', choices=contactReasonList)

    message = TextAreaField(label='your message')
    submit = SubmitField(label='send message')