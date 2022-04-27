from flask import Flask, template_rendered
app = Flask(__name__)

@app.route('/')
def mainPage():
    return'Hello'

@app.route('/help')
def help():
    return'help'

@app.errorhandler(404)
def not_found(e):
    return '404'
