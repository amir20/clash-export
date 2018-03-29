import re

from flask import render_template

from clashleaders import app, cache
from clashleaders.model import ClanPreCalculated


@app.route("/verified/<tag>")
@cache.cached(timeout=86400)
def verified_clans(tag):
    clans = ClanPreCalculated.objects(verified_accounts=tag).order_by('-clanPoints')
    for c in clans:
        c.description = replace_description(c)
    return render_template('verified.html', clans=clans)


def replace_description(clan):
    return re.sub(r"((reddit.com)?(/r/\w+))", r'<a href="https://www.reddit.com\3/" target="_blank">\1</a>',
                  clan.description,
                  flags=re.IGNORECASE)
