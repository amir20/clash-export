import contentful

from flask import render_template

from clashleaders import app, cache

client = contentful.Client('zmnodi6xws9d', '8017b7370aaf68e6caefc204d56fc6f2b3cee22adc907ebf0b4fbc40d7d98799')


@app.context_processor
def inject_changelog():
    logs = fetch_changelog()
    return dict(changelog=[e['raw']['fields'] for e in logs])


@app.route("/changelog")
def changelog():
    return render_template('changelog.html')


@app.route("/privacy")
def privacy():
    return render_template('privacy.html')


@app.route("/terms")
def terms():
    return render_template('terms.html')


@app.route("/about")
def about():
    return render_template('about.html')


@cache.cached(timeout=90, key_prefix='changelog')
def fetch_changelog():
    return list(client.entries({'content_type': 'changelog'}))
