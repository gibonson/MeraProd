from mainApp import db

# EventType Class/Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idEvent = db.Column(db.Integer)
    eventName = db.Column(db.String(20), unique=True)

    def __init__(self, idEvent, eventName):
        self.idEvent = idEvent
        self.eventName = eventName