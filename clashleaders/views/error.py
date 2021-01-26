from flask import render_template

from clashleaders import app
from flask_wtf.csrf import CSRFError


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error_500(e):
    return render_template("500.html"), 500


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template("500.html", reason=e.description), 401
