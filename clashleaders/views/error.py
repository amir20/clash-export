from flask import render_template
from flask.globals import request
from flask_wtf.csrf import CSRFError

from clashleaders import app


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error_500(e):
    return render_template("500.html"), 500


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    if request.accept_mimetypes["application/json"]:
        return dict(error=e.description), 401
    else:
        return render_template("500.html", reason=e.description), 401
