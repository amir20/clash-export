from flask import render_template

from clashleaders import app, cache
from clashleaders.model import Clan
from clashleaders.text.clan_description_processor import transform_description
from clashleaders.views.explore import ORDER_MAPPING


@app.route("/country/<code>", defaults={"sort": "trophies"})
@app.route("/country/<code>/<sort>")
@cache.cached(600)
def country_clans(code, sort):
    if clans := list(Clan.objects(location__countryCode=code.upper()).order_by(ORDER_MAPPING[sort]).limit(50)):
        return render_template("country.html", clans=clans, name=clans[0].location["name"], sort=sort, code=code)
    else:
        return render_template("404.html"), 404
