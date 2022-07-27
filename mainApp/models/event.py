from mainApp import db
from mainApp.models.product import Product
from mainApp.models.user import User
from mainApp.models.status import Status

# Event Class/Model


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idProd = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=True)
    idStatus = db.Column(db.Integer, db.ForeignKey(Status.id))
    startDate = db.Column(db.TIMESTAMP)
    endDate = db.Column(db.TIMESTAMP)
    okCounter = db.Column(db.Integer)
    nokCounter = db.Column(db.Integer)
    userID = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, idProd, idStatus, startDate, endDate, okCounter, nokCounter, userID):
        self.idProd = idProd
        self.idStatus = idStatus
        self.startDate = startDate
        self.endDate = endDate
        self.okCounter = okCounter
        self.nokCounter = nokCounter
        self.userID = userID

    def sub(self, endDate, startDate):
        return(endDate - startDate)
