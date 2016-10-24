from flask import Flask, request, redirect, url_for, send_file, render_template
import os
from io import BytesIO
import api

app = Flask(__name__)
app.debug = os.getenv('DEBUG', False)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/search")
def search():
    clan = api.clan(request.args.get('tag'))

    if 'tag' in clan:
        return redirect(url_for('clan_detail', tag=clan['tag']))
    else:
        return 'error'


@app.route("/clan/<path:tag>")
def clan_detail(tag):
    if tag.endswith(".xlsx"):
        return export(tag=tag[:-5], filename=tag)
    else:
        return render_template('clan.html', clan=api.clan(tag))


def export(tag, filename):
    output = BytesIO()
    api.export(tag, output)
    output.seek(0)
    return send_file(output, attachment_filename=filename, as_attachment=True)


if __name__ == "__main__":
    app.run()
