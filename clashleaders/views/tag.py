from flask import render_template

from clashleaders import app
from clashleaders.model import Clan


@app.route("/tag/<tag>")
def tagged_clans(tag):
    tag = f"#{tag}"
    if clans := list(Clan.objects.search_text(f'"{tag}"')):
        return render_template("tag.html", clans=clans, tag=tag)
    else:
        return render_template("404.html"), 404
