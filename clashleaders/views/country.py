from flask import render_template

from clashleaders import app, cache
from clashleaders.model import ClanPreCalculated
from clashleaders.text.clan_description_processor import transform_description


@app.route("/country/<code>")
@cache.cached(timeout=1000)
def country_clans(code):
    code = code.upper()
    clans = ClanPreCalculated.objects(location__countryCode=code).order_by('-clanPoints').limit(50)
    for c in clans:
        c.description = transform_description(c.description)

    return render_template('country.html', clans=clans, name=clans[0].location['name'])
