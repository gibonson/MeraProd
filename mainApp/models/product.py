from mainApp import db

# Product Class/Model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelNumber = db.Column(db.String(20), unique=True)
    modelName = db.Column(db.String(20))
    orderStatus = db.Column(db.String(20))
    startDate = db.Column(db.TIMESTAMP)
    executionDate = db.Column(db.TIMESTAMP)

    def __init__(self, modelNumber, modelName, orderStatus, startDate, executionDate):
        self.modelNumber = modelNumber
        self.modelName = modelName
        self.singleOrDouble = singleOrDouble
        self.orderStatus = orderStatus
        self.startDate = startDate
        self.executionDate = executionDate
