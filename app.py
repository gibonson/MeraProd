from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/help')
def help():
    return'help'

@app.errorhandler(404)
def not_found(e):
    return '404'
