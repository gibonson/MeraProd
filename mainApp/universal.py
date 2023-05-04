from mainApp.models.product import Product
from mainApp.models.event import Event

def openProductsCounter():
    openProductCounter = 0
    activProductsList = Product.query.filter(Product.orderStatus == "Open")
    for activProductList in activProductsList:
        openProductCounter += 1
    return openProductCounter


def openEventsCounter():
    openEventCounter = 0
    activEventsList = Event.query.filter(Event.endDate == None)
    for activEventList in activEventsList:
        openEventCounter += 1
    return openEventCounter
