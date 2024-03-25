from flask import render_template

from clashleaders import app


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/about")
def about():
    return render_template("about.html")
