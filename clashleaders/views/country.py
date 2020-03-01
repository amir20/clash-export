from flask import render_template

from clashleaders import app, cache
from clashleaders.model import Clan
from clashleaders.text.clan_description_processor import transform_description


@app.route("/country/<code>")
def country_clans(code):
    code = code.upper()
    clans = fetch_country(code)

    if clans:
        return render_template("country.html", clans=clans, name=clans[0].location["name"])
    else:
        return render_template("404.html"), 404


@cache.memoize(600)
def fetch_country(code):
    clans = Clan.objects(location__countryCode=code).order_by("-clanPoints").limit(50)
    for c in clans:
        c.description = transform_description(c.description)

    return clans
