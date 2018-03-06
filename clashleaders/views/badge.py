import base64

import requests
from flask import make_response, render_template
from mongoengine import DoesNotExist

from clashleaders import app
from clashleaders.model import ClanPreCalculated


@app.route("/clan/<slug>.svg")
def clan_detail_svg(slug):
    try:
        clan = ClanPreCalculated.find_by_slug(slug)
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        response = make_response(render_template('clan.svg', clan=clan))
        response.headers['Content-type'] = "image/svg+xml"
        return response


def badge_base64(url):
    r = requests.get(url)
    return "data:image/png;base64," + str(base64.b64encode(r.content).decode("utf-8"))
