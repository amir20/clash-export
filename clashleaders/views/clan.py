from flask import jsonify, render_template, request
from inflection import camelize
from mongoengine import DoesNotExist

from clashleaders import app, cache
from clashleaders.insights.clan_activity import clan_status
from clashleaders.model import Clan, Status
from clashleaders.text.clan_description_processor import transform_description
from clashleaders.views.player import player_score


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
    return jsonify(Clan.find_by_tag(tag).historical_near_days_ago(request.args.get('daysAgo', 0)).to_matrix())


@app.route("/clan/<tag>/refresh.json")
def clan_refresh_json(tag):
    clan = Clan.fetch_and_update(tag, sync_calculation=False)
    clan.update(inc__page_views=1)
    player_data = clan.historical_near_now().to_matrix()
    players_status = clan_status(clan)

    player_score.delete_memoized()  # We should clear the cache so old player score are thrown away

    return jsonify(dict(
        playerData=player_data,
        playersStatus=players_status
    ))


@app.route("/clan/<tag>/long.json")
def clan_long_json(tag):
    clan = Clan.find_by_tag(tag)

    data = dict(clan.to_mongo())
    data['computed'] = dict(data['computed'])
    data['day_delta'] = dict(data['day_delta'])
    data['week_delta'] = dict(data['week_delta'])
    del data['memberList']
    del data['_id']

    return jsonify(data)


@app.route("/clan/<slug>")
def clan_detail_page(slug):
    try:
        clan = Clan.find_by_slug(slug)
        description = transform_description(clan.description)
        players = clan.historical_near_now().to_matrix()
        start_count, similar_clans = clan.similar_clans()
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        return render_template('clan.html',
                               clan=clan,
                               players=players,
                               description=description,
                               oldest_days=clan.days_of_history(),
                               similar_clans=similar_clans,
                               similar_clans_start_count=start_count)


@app.route("/clan/<tag>/stats.json")
@cache.cached(timeout=1200, query_string=True)
def clan_stats(tag):
    clan = Clan.find_by_tag(tag)
    previous_clan = clan.historical_near_days_ago(request.args.get('daySpan', 7))
    delta = clan.historical_near_now().clan_delta(previous_clan)

    return jsonify(dict(gold_grab=delta.avg_gold_grab,
                        elixir_grab=delta.avg_elixir_grab,
                        de_grab=delta.avg_de_grab))


@app.route("/clan/<tag>/short.json")
@cache.cached(timeout=1000)
def clan_short_json(tag):
    clan = Clan.find_by_tag(tag)
    df = clan.historical_near_now().to_df()[['Name', 'TH Level', 'Current Trophies']].reset_index()
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
    df = Clan.find_by_tag(tag).to_historical_df()[['members', 'clanPoints']].resample('D').mean().dropna()
    return df.to_json(orient='columns', date_format='iso')
