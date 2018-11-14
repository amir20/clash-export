from flask import render_template

from clashleaders import app, cache
from clashleaders.model import ClanPreCalculated
from clashleaders.text.clan_description_processor import transform_description


@app.route("/verified/<tag>")
def verified_clans(tag):
    clans = fetch_clans(tag)
    for c in clans:
        c.description = transform_description(c.description)

    return render_template('verified.html', clans=clans)


@cache.memoize(300)
def fetch_clans(tag):
    return ClanPreCalculated.objects(verified_accounts=tag).order_by('-clanPoints')
