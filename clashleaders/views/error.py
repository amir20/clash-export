from flask import render_template

from clashleaders import app


@app.errorhandler(404)
def error_404(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def error_500(e):
    return render_template("500.html"), 500
