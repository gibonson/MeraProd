from mainApp import db

# Status Class/Model


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statusCode = db.Column(db.Integer)
    statusName = db.Column(db.String(20), unique=True)
    production = db.Column(db.String(20))

    def __init__(self, statusCode, statusName, production):
        self.statusCode = statusCode
        self.statusName = statusName
        self.production = production
