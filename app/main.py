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
    return redirect(url_for('clan_detail', tag=request.args.get('tag')))


@app.route("/clan/<path:tag>")
def clan_detail(tag):
    is_export = False

    if tag.endswith(".xlsx"):
        tag = tag[:-5]
        is_export = True

    clan = api.search_by_tag(tag)

    if 'tag' not in clan:
        return render_template('error.html'), 404
    elif is_export:
        return export(clan=clan, filename='%s.xlsx' % tag)
    else:
        return render_template('clan.html', clan=clan)


def export(clan, filename):
    output = BytesIO()
    api.export(clan, output)
    output.seek(0)
    return send_file(output, attachment_filename=filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=80)
