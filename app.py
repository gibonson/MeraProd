from flask import Flask
app = Flask(__name__)

@app.route('/')
def mainPage():
    return'Hello'

@app.route('/help')
def help():
    return'help'