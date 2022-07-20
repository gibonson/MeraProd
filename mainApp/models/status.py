from mainApp import db

# Status Class/Model


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    statusID = db.Column(db.Integer)
    statusName = db.Column(db.String(20), unique=True)
    production = db.Column(db.String(20))

    def __init__(self, statusID, statusName, production):
        self.statusID = statusID
        self.statusName = statusName
        self.production = production
