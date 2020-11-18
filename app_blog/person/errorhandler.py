from flask import render_template
from . import person

@person.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404