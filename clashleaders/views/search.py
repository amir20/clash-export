from flask import jsonify, request

from clashleaders import app, csrf
from clashleaders.clash import api
from clashleaders.clash.transformer import to_short_clan
from clashleaders.model import Clan


@app.route("/search.json", methods=["POST"])
def search():
    query = request.json["q"]
    try:
        clan = api.find_clan_by_tag(query)
        results = [Clan(**clan)]
    except api.ClanNotFound:
        results = [Clan(**c) for c in api.search_by_name(query, limit=6)]
    except api.ApiException:
        return jsonify([]), 500

    results = sorted(results, key=lambda c: c.members, reverse=True)
    return jsonify([to_short_clan(c)._asdict() for c in results])
