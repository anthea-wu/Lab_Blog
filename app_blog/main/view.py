from flask import render_template, redirect
from . import main

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')