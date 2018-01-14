import re

from flask import render_template, send_file, request, jsonify
from mongoengine import DoesNotExist

from clashleaders import app, cache
from clashleaders.clash import excel, api
from clashleaders.clash.calculation import update_calculations
from clashleaders.clash.transformer import transform_players, to_short_clan
from clashleaders.model import Clan, ClanPreCalculated

URL_REGEX = re.compile(r"(https?://)?([a-zA-Z0-9]+\.)?([a-zA-Z0-9]+\.(com|net|org|edu|uk|jp|ir|ru|us|ca|gg|gl|ly|co|me)[^\s]*)", re.IGNORECASE)


@app.route("/search.json")
def search():
    query = request.args.get('q')
    try:
        clan = api.find_clan_by_tag(query)
        results = [Clan(**clan)]
    except api.ClanNotFound:
        results = [Clan(**c) for c in api.search_by_name(query, limit=6)]

    results = sorted(results, key=lambda c: c.members, reverse=True)
    return jsonify([to_short_clan(c)._asdict() for c in results])


@app.route("/clan/<tag>.json")
def clan_detail_json(tag):
    try:
        api.find_clan_by_tag(tag)
    except api.ClanNotFound:
        return render_template('error.html'), 404
    else:
        days_ago = request.args.get('daysAgo')
        clan = clan_from_days_ago(days_ago, tag)
        return jsonify(transform_players(clan.players))


@app.route("/clan/<slug>.xlsx")
def clan_detail_xlsx(slug):
    try:
        clan = ClanPreCalculated.find_by_slug(slug)
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        days_ago = request.args.get('daysAgo')
        clan = clan_from_days_ago(days_ago, clan.tag)
        return send_file(excel.to_stream(clan), attachment_filename=f"{clan.tag}.xlsx", as_attachment=True)


@app.route("/clan/<slug>")
def clan_detail_page(slug):
    try:
        clan = ClanPreCalculated.find_by_slug(slug)
        most_recent = Clan.find_first_by_tag(clan.tag)
        players = transform_players(most_recent.players)
        description = URL_REGEX.sub(repl, clan.description)
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        return render_template('clan.html', clan=clan, players=players, description=description)


@app.route("/clan/<tag>/short.json")
@cache.cached(timeout=1000)
def clan_meta(tag):
    try:
        clan = ClanPreCalculated.find_by_tag(tag)
    except DoesNotExist:
        clan = update_calculations(Clan.fetch_and_save(tag))

    data = {
        'tag': clan.tag,
        'slug': clan.slug,
        'name': clan.name,
        'description': clan.description,
        'clanPoints': clan.clanPoints,
        'clanVersusPoints': clan.clanVersusPoints,
        'members': clan.members,
        'badgeUrls': clan.badgeUrls,
    }

    return jsonify(data)


def clan_from_days_ago(days_ago, tag):
    if days_ago:
        return Clan.from_now_with_tag(tag, days=int(days_ago)).first() or Clan.fetch_and_save(tag)
    else:
        return Clan.fetch_and_save(tag)


def repl(match):
    if match.group(0).startswith('http'):
        return f"<a href=\"{match.group(0)}\" target=\"_blank\">{match.group(0)}</a>"
    else:
        return f"<a href=\"http://{match.group(0)}\" target=\"_blank\">{match.group(0)}</a>"
