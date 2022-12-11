from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField,TextAreaField

class EmailForm(FlaskForm):

    contactReasonList = [("Niepoprawny kod zlecenia", "Niepoprawny kod zlecenia"),
                     ("Pomyłka w ilości OK/NOK", "Pomyłka w ilości OK/NOK"),
                     ("Niezarejestrowane kody przestoju podczas zlecenia", "Niezarejestrowane kody przestoju podczas zlecenia"),
                     ("Brak połączenia z systemem przez dany okres czasu", "Brak połączenia z systemem przez dany okres czasu"),
                     ("Błąd systemu", "Błąd systemu"),
                     ("INNE - OPISZ", "INNE - OPISZ")]


    id = StringField(label="Model Code:")

    contactReason = SelectField(
        label='Contact Reason:', choices=contactReasonList)

    message = TextAreaField(label='Your message')
    submit = SubmitField(label='Send message')