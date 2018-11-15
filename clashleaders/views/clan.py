import pandas as pd
from flask import jsonify, render_template, request, send_file
from mongoengine import DoesNotExist
from user_agents import parse

from clashleaders import app, cache
from clashleaders.clash import api, excel
from clashleaders.clash.clan_calculation import calculate_delta
from clashleaders.clash.player_calculation import clan_status
from clashleaders.model import Clan, ClanPreCalculated, Status
from clashleaders.text.clan_description_processor import transform_description


@app.context_processor
def inject_most_popular():
    status = Status.get_instance()
    return dict(status=status,
                most_popular=status.popular_clans,
                popular_countries=status.top_countries,
                reddit_clans=status.reddit_clans
                )


@app.route("/clan/<tag>.json")
def clan_detail_json(tag):
    try:
        days_ago = request.args.get('daysAgo')
        clan = clan_from_days_ago(days_ago, tag)
        return jsonify(clan.to_player_matrix())
    except api.ClanNotFound:
        return jsonify(dict(error=f"{tag} not found")), 404
    except api.ApiTimeout:
        return jsonify(dict(error=f"API timed out while fetching all players for {tag}")), 504
    except api.ApiException:
        return jsonify(dict(error=f"Clash of Clans API is down right now.")), 500


@app.route("/clan/<tag>/refresh.json")
def clan_refresh_json(tag):
    clan = Clan.fetch_and_save(tag)
    cpc = clan.pre_calculated()
    player_data = clan.to_player_matrix()
    players_status = clan_status(cpc)

    return jsonify(dict(playerData=player_data, playersStatus=players_status))


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
        clan = None
        clan = ClanPreCalculated.find_by_slug(slug)
        update_page_views(clan)
        description = transform_description(clan.description)
        players = clan.most_recent.to_player_matrix()
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
def clan_stats(tag):
    days = int(request.args.get('daysAgo', 7))

    cpc = ClanPreCalculated.find_by_tag(tag)
    start_df = cpc.previous_data(days=days).to_data_frame()
    now_df = cpc.most_recent.to_data_frame()
    delta = calculate_delta(now_df, start_df)
    gold = delta.avg_gold_grab
    elixir = delta.avg_elixir_grab
    de = delta.avg_de_grab

    data = {
        'gold_grab': gold,
        'elixir_grab': elixir,
        'de_grab': de,
        'name': cpc.name
    }

    return jsonify(data)


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


def clan_from_days_ago(days_ago, tag):
    if days_ago:
        return Clan.from_now_with_tag(tag, days=int(days_ago)).first() or Clan.fetch_and_save(tag)
    else:
        try:
            return Clan.fetch_and_save(tag)
        except api.TooManyRequests:
            return Clan.find_most_recent_by_tag(tag)


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
