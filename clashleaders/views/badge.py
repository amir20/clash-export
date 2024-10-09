import base64
from io import BytesIO

import requests
from cairosvg import svg2png
from flask import make_response, render_template, send_file
from mongoengine import DoesNotExist

from clashleaders import app, cache
import clashleaders.model.clan

TEMPLATE = dict(small="badges/small.svg", large="badges/large.svg")


@app.route("/b/<size>/<tag>.svg")
@cache.cached(timeout=10800)
def clan_badge_svg(size, tag):
    template = TEMPLATE.get(size)
    svg = render_as_svg(template, tag)
    response = make_response(svg)
    response.headers["Content-type"] = "image/svg+xml"
    return response


@app.route("/b/<size>/<tag>.png")
@cache.cached(timeout=10800)
def clan_badge_png(size, tag):
    template = TEMPLATE.get(size)
    svg = render_as_svg(template, tag)
    png = svg2png(bytestring=svg)
    return send_file(BytesIO(png), mimetype="image/png")


def render_as_svg(template, tag):
    try:
        clan = clashleaders.model.clan.Clan.find_by_tag(tag)
    except DoesNotExist:
        return render_template("404.html"), 404
    else:
        return render_template(template, clan=clan)


def badge_base64(url):
    r = requests.get(url)
    return "data:image/png;base64," + str(base64.b64encode(r.content).decode("utf-8"))


app.add_template_global(badge_base64, "base64_png")
