import re

from flask import jsonify, render_template, request, send_file
from mongoengine import DoesNotExist
from user_agents import parse

from clashleaders import app, cache
from clashleaders.clash import api, excel
from clashleaders.clash.transformer import to_short_clan, transform_players
from clashleaders.model import Clan, ClanPreCalculated

URL_REGEX = re.compile(
    r"(https?://)?([a-zA-Z0-9]+\.)?([a-zA-Z0-9]+\.(com|net|org|edu|uk|jp|ir|ru|us|ca|gg|gl|ly|co|me|gd)[^\s]*)",
    re.IGNORECASE)


@app.context_processor
def inject_most_popular():
    return dict(most_popular=ClanPreCalculated.objects.order_by('-page_views').limit(6))


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
        update_page_views(clan)
        description = clan_description(clan)
        players = transform_players(clan.most_recent.players)
        delta = compute_oldest_days(clan)
        similar_clans = find_similar_clans(clan)
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        return render_template('clan.html', clan=clan, players=players, description=description, oldest_days=delta.days,
                               similar_clans=similar_clans)


@app.route("/clan/<tag>/short.json")
@cache.cached(timeout=1000)
def clan_meta(tag):
    try:
        clan = ClanPreCalculated.find_by_tag(tag)
    except DoesNotExist:
        clan = Clan.fetch_and_save(tag).update_calculations()

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


def update_page_views(clan):
    user_agent = parse(request.user_agent.string)
    if not user_agent.is_bot:
        clan.update(inc__page_views=1)


def compute_oldest_days(clan):
    most_recent = clan.most_recent
    least_recent = Clan.find_last_by_tag(clan.tag)
    return most_recent.id.generation_time - least_recent.id.generation_time


def clan_description(clan):
    return URL_REGEX.sub(repl, clan.description)


def repl(match):
    if match.group(0).startswith('http'):
        return f"<a href=\"{match.group(0)}\" target=\"_blank\">{match.group(0)}</a>"
    else:
        return f"<a href=\"http://{match.group(0)}\" target=\"_blank\">{match.group(0)}</a>"


def find_similar_clans(clan):
    less = ClanPreCalculated.objects(cluster_label=clan.cluster_label, clanPoints__lt=clan.clanPoints).order_by('-clanPoints').limit(2)
    more = ClanPreCalculated.objects(cluster_label=clan.cluster_label, clanPoints__gt=clan.clanPoints).order_by('clanPoints').limit(2)

    return sorted([*less, clan, *more], key=lambda c: c.clanPoints)
