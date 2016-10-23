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


@app.route("/clan/<tag>")
def clan_detail(tag):
    clan = api.clan(tag)
    return render_template('clan.html', clan=clan)


@app.route("/clan/<tag>/export")
def clan_export(tag):
    output = BytesIO()
    api.export(tag, output)
    output.seek(0)
    return send_file(output, attachment_filename="testing.xlsx", as_attachment=True)


if __name__ == "__main__":
    app.run()
