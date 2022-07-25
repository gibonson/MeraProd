from mainApp import db

# Product Class/Model


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    modelCode = db.Column(db.String(20), unique=True)
    modelName = db.Column(db.String(20))
    orderStatus = db.Column(db.String(20))
    startDate = db.Column(db.Integer)
    executionDate = db.Column(db.Integer)

    def __init__(self, modelCode, modelName, orderStatus, startDate, executionDate):
        self.modelCode = modelCode
        self.modelName = modelName
        self.orderStatus = orderStatus
        self.startDate = startDate
        self.executionDate = executionDate
