from datetime import datetime
from time import sleep

from flask import jsonify, render_template, request
from inflection import camelize
from mongoengine import DoesNotExist
from rq.exceptions import NoSuchJobError
from rq.job import Job

from clashleaders import app, cache, redis_connection
from clashleaders.insights.clan_activity import clan_status
from clashleaders.model import Clan, Status
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
    return jsonify(Clan.find_by_tag(tag).historical_near_days_ago(request.args.get('daysAgo', 0)).to_matrix())


@app.route("/clan/<tag>/refresh.json")
def clan_refresh_json(tag):
    clan = Clan.fetch_and_update(tag, sync_calculation=False)
    clan.update(inc__page_views=1)
    player_data = clan.historical_near_now().to_matrix()
    players_status = clan_status(clan)

    return jsonify(dict(
        playerData=player_data,
        playersStatus=players_status,
        jobId=clan.job.id
    ))


@app.route("/clan/<tag>/long.json")
def clan_long_json(tag):
    job_id = request.args.get('jobId')

    if job_id:
        start = datetime.now()
        while (datetime.now() - start).total_seconds() < 2:
            sleep(0.2)
            try:
                Job.fetch(job_id, connection=redis_connection)
            except NoSuchJobError:
                break

    clan = Clan.find_by_tag(tag)
    return jsonify(clan.to_dict())


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
    keys = {'tag', 'slug', 'name', 'description', 'clanPoints', 'clanVersusPoints', 'members', 'badgeUrls'}
    data = clan.to_dict()
    data = {k: v for k, v in data.items() if k in keys}
    data['players'] = list(players)

    return jsonify(data)


@app.route("/clan/<tag>/trophies.json")
@cache.cached(timeout=1000)
def clan_trophies(tag):
    df = Clan.find_by_tag(tag).to_historical_df()[['members', 'clanPoints']].resample('D').mean().dropna()
    return df.to_json(orient='columns', date_format='iso')
