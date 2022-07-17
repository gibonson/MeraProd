from mainApp import db

# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    belegNumber = db.Column(db.String(20), unique=True)
    modelName = db.Column(db.String(20))
    lenght = db.Column(db.Integer)
    numberOfParts = db.Column(db.Integer)
    bracket = db.Column(db.Boolean)
    singleOrDouble = db.Column(db.Integer)
    orderStatus = db.Column(db.Integer)
    executionDate = db.Column(db.DateTime)

    def __init__(self, belegNumber, modelName, lenght, numberOfParts, bracket, singleOrDouble, orderStatus, executionDate):
        self.belegNumber = belegNumber
        self.modelName = modelName
        self.lenght = lenght
        self.numberOfParts = numberOfParts
        self.bracket = bracket
        self.singleOrDouble = singleOrDouble
        self.orderStatus = orderStatus
        self.executionDate = executionDate