import re
import pandas as pd

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
        return jsonify(transform_players(clan.players_data()))


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
        players = transform_players(clan.most_recent.players_data())
        start_count, similar_clans = find_similar_clans(clan)
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        return render_template('clan.html', clan=clan,
                               players=players,
                               description=description,
                               oldest_days=clan.days_span,
                               similar_clans=similar_clans,
                               similar_clans_start_count=start_count)


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


@app.route("/clan/<tag>/trophies.json")
@cache.cached(timeout=1000)
def clan_trophies(tag):
    data = list(Clan.from_now_with_tag(tag, days=28).no_cache().only('clanPoints'))
    dates = [s.id.generation_time for s in data]
    points = [s.clanPoints for s in data]
    series = pd.Series(points, index=dates)
    resampled = series.resample('D').mean().dropna()
    map = {key.strftime("%Y-%m-%d"): value for key, value in resampled.items()}

    return jsonify(dict(labels=list(map.keys()), points=list(map.values())))


def clan_from_days_ago(days_ago, tag):
    if days_ago:
        return Clan.from_now_with_tag(tag, days=int(days_ago)).first() or Clan.fetch_and_save(tag)
    else:
        return Clan.fetch_and_save(tag)


def update_page_views(clan):
    user_agent = parse(request.user_agent.string)
    if not user_agent.is_bot:
        clan.update(inc__page_views=1)


def clan_description(clan):
    return URL_REGEX.sub(repl, clan.description)


def repl(match):
    if match.group(0).startswith('http'):
        return f"<a href=\"{match.group(0)}\" target=\"_blank\">{match.group(0)}</a>"
    else:
        return f"<a href=\"http://{match.group(0)}\" target=\"_blank\">{match.group(0)}</a>"


def find_similar_clans(clan):
    less = ClanPreCalculated.objects(cluster_label=clan.cluster_label, clanPoints__lt=clan.clanPoints).order_by('-clanPoints').limit(4)
    more = ClanPreCalculated.objects(cluster_label=clan.cluster_label, clanPoints__gt=clan.clanPoints).order_by('clanPoints').limit(2)

    clans = sorted([*less, clan, *more], key=lambda c: c.clanPoints, reverse=True)[:5]
    start_count = ClanPreCalculated.objects(cluster_label=clan.cluster_label, clanPoints__gt=clans[0].clanPoints).count() + 1

    return start_count, clans
