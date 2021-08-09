import contentful
from flask import render_template

from clashleaders import app, cache


@app.context_processor
def inject_changelog():
    logs = fetch_changelog()
    changes = [{"id": e.id, "slug": e.slug, "title": e.title, "summary": e.summary, "publishedOn": e.published_on} for e in logs]
    return dict(updates=changes)


@app.route("/updates")
def updates():
    return render_template("updates.html", changelog=fetch_changelog())


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/about")
def about():
    return render_template("about.html")


@cache.memoize(600)
def fetch_changelog():
    client = contentful.Client("zmnodi6xws9d", "8017b7370aaf68e6caefc204d56fc6f2b3cee22adc907ebf0b4fbc40d7d98799")
    return list(client.entries({"content_type": "changelog", "order": "-fields.publishedOn"}))
