from datetime import timedelta, datetime

import pandas as pd
from flask import jsonify, render_template, request
from inflection import camelize
from mongoengine import DoesNotExist
from user_agents import parse

from clashleaders import app, cache
from clashleaders.clash.player_calculation import clan_status
from clashleaders.model import Clan, Status, HistoricalClan
from clashleaders.text.clan_description_processor import transform_description


@app.context_processor
def inject_most_popular():
    status = Status.get_instance()
    return dict(status=status,
                most_popular=[],
                popular_countries=[],
                reddit_clans=[]
                )


@app.route("/clan/<tag>.json")
def clan_detail_json(tag): return jsonify(clan_near_days_ago(request.args.get('daysAgo', 0), tag).to_matrix())


@app.route("/clan/<tag>/refresh.json")
def clan_refresh_json(tag):
    clan = Clan.fetch_and_update(tag)
    player_data = clan.historical_near_now().to_matrix()
    players_status = {}
    return jsonify(dict(playerData=player_data, playersStatus=players_status))


@app.route("/clan/<slug>")
def clan_detail_page(slug):
    try:
        clan = None
        clan = Clan.find_by_slug(slug)
        update_page_views(clan)
        description = transform_description(clan.description)
        players = clan.to_matrix()
        start_count, similar_clans = find_similar_clans(clan)
    except DoesNotExist:
        if clan:
            clan = Clan.fetch_and_save(clan.tag).update_calculations()
            return clan_detail_page(clan.slug)
        else:
            return render_template('error.html'), 404
    else:
        return render_template('clan.html', clan=clan,
                               players=players,
                               description=description,
                               last_updated=clan.last_updated,
                               oldest_days=clan.days_span,  # TODO
                               similar_clans=similar_clans,
                               similar_clans_start_count=start_count)


@app.route("/clan/<tag>/stats.json")
@cache.cached(timeout=1200, query_string=True)
def clan_stats(tag):
    clan = clan_near_days_ago(request.args.get('daysAgo', 0), tag)
    return jsonify(clan.week_delta)


@app.route("/clan/<tag>/short.json")
@cache.cached(timeout=1000)
def clan_meta(tag):
    clan = ClanPreCalculated.find_or_create_by_tag(tag)
    df = clan.most_recent.to_data_frame()[['Name', 'TH Level', 'Current Trophies']].reset_index()
    players = df.rename(lambda s: camelize(s.replace(" ", ""), False), axis='columns').to_dict('i').values()

    data = {
        'tag': clan.tag,
        'slug': clan.slug,
        'name': clan.name,
        'description': clan.description,
        'clanPoints': clan.clanPoints,
        'clanVersusPoints': clan.clanVersusPoints,
        'members': clan.members,
        'badgeUrls': clan.badgeUrls,
        'players': list(players)
    }

    return jsonify(data)


@app.route("/clan/<tag>/trophies.json")
@cache.cached(timeout=1000)
def clan_trophies(tag):
    clans = list(Clan.from_now_with_tag(tag, days=28).no_cache().only('clanPoints', 'members'))
    data = [[c.members, c.clanPoints] for c in clans]
    df = pd.DataFrame(data, index=pd.to_datetime([s.id.generation_time for s in clans]),
                      columns=['members', 'trophies'])
    resampled = df.resample('D').mean().dropna()
    data = dict(
        dates=[i.strftime("%Y-%m-%d") for i in resampled.index],
        members=resampled['members'].values.tolist(),
        trophies=resampled['trophies'].values.tolist()
    )

    return jsonify(data)


@app.route("/clan/<tag>/chart.json")
@cache.cached(timeout=1000)
def clan_chart(tag):
    data = list(Clan.from_now_with_tag(tag, days=28).no_cache().only('clanPoints', 'avg_gold_grab'))
    dates = [s.id.generation_time for s in data]
    columns = [dict(points=s.clanPoints, gold=getattr(s, 'avg_gold_grab', 0)) for s in data]
    df = pd.DataFrame(columns, index=dates)
    resampled = df.resample('D').mean().dropna()
    labels = [k.strftime("%Y-%m-%d") for k in resampled.index.tolist()]

    return jsonify(
        dict(labels=labels,
             points=resampled['points'].values.tolist(),
             avg_gold=resampled['gold'].values.tolist()))


def update_page_views(clan):
    user_agent = parse(request.user_agent.string)
    if not user_agent.is_bot:
        clan.update(inc__page_views=1)


def find_similar_clans(clan):
    less = ClanPreCalculated.objects(cluster_label=clan.cluster_label, clanPoints__lt=clan.clanPoints).order_by(
        '-clanPoints').limit(4)
    more = ClanPreCalculated.objects(cluster_label=clan.cluster_label, clanPoints__gt=clan.clanPoints).order_by(
        'clanPoints').limit(2)

    clans = sorted([*less, clan, *more], key=lambda c: c.clanPoints, reverse=True)[:5]
    start_count = ClanPreCalculated.objects(cluster_label=clan.cluster_label,
                                            clanPoints__gt=clans[0].clanPoints).count() + 1

    return start_count, clans


def clan_near_days_ago(days_ago, tag):
    dt = datetime.now() - timedelta(days=int(days_ago))
    return HistoricalClan.find_by_tag_near_time(tag=tag, dt=dt)
