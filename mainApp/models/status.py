from mainApp import db
from mainApp.models.product import Product
from mainApp.models.user import User

# Status Class/Model
class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProd = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=True)
    idEvent = db.Column(db.Integer)
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    okCounter = db.Column(db.Integer)
    nokCounter = db.Column(db.Integer)
    userID = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, idProd, idEvent, startDate, endDate, okCounter, nokCounter, userID):
        self.idProd = idProd
        self.idEvent = idEvent
        self.startDate = startDate
        self.endDate = endDate
        self.okCounter = okCounter
        self.nokCounter = nokCounter
        self.userID = userID

    def sub(self, endDate, startDate):
        return(endDate - startDate)