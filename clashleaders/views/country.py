from flask import render_template

from clashleaders import app, cache
from clashleaders.model import Clan
from clashleaders.text.clan_description_processor import transform_description
from clashleaders.views.explore import ORDER_MAPPING


@app.route("/country/<code>", defaults={"sort": "trophies"})
@app.route("/country/<code>/<sort>")
@cache.cached(600)
def country_clans(code, sort):
    clans = fetch_country(code.upper(), sort)

    if clans:
        return render_template("country.html", clans=clans, name=clans[0].location["name"], sort=sort, code=code)
    else:
        return render_template("404.html"), 404


def fetch_country(code, sort):
    clans = list(Clan.objects(location__countryCode=code).order_by(sort).limit(50))
    for c in clans:
        c.description = transform_description(c.description)

    return clans
