from flask import render_template

from clashleaders import app, cache
from clashleaders.model import Clan
from clashleaders.views.explore import ORDER_MAPPING, TITLE_MAPPING


@app.route("/country/<code>", defaults={"sort": "trophies"})
@app.route("/country/<code>/<sort>")
@cache.cached(600)
def country_clans(code, sort):
    if clans := list(
        Clan.objects(location__countryCode=code.upper(), active_members__gte=10)
        .order_by(ORDER_MAPPING[sort])
        .limit(50)
    ):
        title = f"{clans[0].location['name']}'s {TITLE_MAPPING[sort]}"
        return render_template(
            "country.html", clans=clans, title=title, sort=sort, code=code
        )
    else:
        return render_template("404.html"), 404
