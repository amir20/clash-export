import base64

import requests
from flask import make_response, render_template
from mongoengine import DoesNotExist

from clashleaders import app, cache
from clashleaders.model import ClanPreCalculated

TEMPLATE = dict(small="badges/small.svg", large="badges/large.svg")


@app.route("/b/<size>/<tag>.svg")
@cache.cached(timeout=10800)
def clan_detail_svg(size, tag):
    try:
        clan = ClanPreCalculated.find_by_tag(tag)
        template = TEMPLATE.get(size)
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        response = make_response(render_template(template, clan=clan))
        response.headers['Content-type'] = "image/svg+xml"
        return response


def badge_base64(url):
    r = requests.get(url)
    return "data:image/png;base64," + str(base64.b64encode(r.content).decode("utf-8"))


app.add_template_global(badge_base64, 'base64_png')
