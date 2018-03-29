from flask import render_template

from clashleaders import app, cache
from clashleaders.model import ClanPreCalculated
from clashleaders.text.clan_description_processor import transform_description


@app.route("/verified/<tag>")
@cache.cached(timeout=86400)
def verified_clans(tag):
    clans = ClanPreCalculated.objects(verified_accounts=tag).order_by('-clanPoints')
    for c in clans:
        c.description = transform_description(c.description)

    return render_template('verified.html', clans=clans)
