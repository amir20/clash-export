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


@app.route("/clan/<slug>")
def clan_detail_page(slug):
    try:
        clan = Clan.find_by_slug(slug)
        description = transform_description(clan.description)
        start_count, similar_clans = clan.similar_clans()
        initial_state = dict(
            name=clan.name,
            tag=clan.tag,
            updatedOn=clan.updated_on,
            historicData=clan.historical_near_days_ago(7).to_matrix(),
            recentData=clan.historical_near_now().to_matrix(),
            playerStatus={}
        )
    except DoesNotExist:
        return render_template('error.html'), 404
    else:
        return render_template('clan.html',
                               clan=clan,
                               initial_state=initial_state,
                               description=description,
                               oldest_days=clan.days_of_history(),
                               similar_clans=similar_clans,
                               similar_clans_start_count=start_count)


# TODO REMOVE
@app.route("/clan/<tag>.json")
def clan_detail_json(tag):
    return jsonify(Clan.find_by_tag(tag).historical_near_days_ago(request.args.get('daysAgo', 0)).to_matrix())


# TODO REMOVE
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


# TODO REMOVE
@app.route("/clan/<tag>/long.json")
def clan_long_json(tag):
    job_id = request.args.get('jobId')

    if job_id:
        wait_for_job(job_id)

    clan = Clan.find_by_tag(tag)
    return jsonify(clan.to_dict())


# TODO REMOVE
@app.route("/clan/<tag>/stats.json")
@cache.cached(timeout=1200, query_string=True)
def clan_stats(tag):
    clan = Clan.find_by_tag(tag)
    previous_clan = clan.historical_near_days_ago(request.args.get('daySpan', 7))
    delta = clan.historical_near_now().clan_delta(previous_clan)

    return jsonify(dict(gold_grab=delta.avg_gold_grab,
                        elixir_grab=delta.avg_elixir_grab,
                        de_grab=delta.avg_de_grab,
                        name=clan.name))


# TODO REMOVE
@app.route("/clan/<tag>/short.json")
@cache.cached(timeout=1000)
def clan_short_json(tag):
    clan = Clan.find_by_tag(tag)
    df = clan.historical_near_now().to_df()[['Name', 'TH Level', 'Current Trophies']].reset_index()
    players = df.rename(lambda s: camelize(s.replace(" ", ""), False), axis='columns').to_dict('i').values()
    data = clan.to_dict(short=True)
    data['players'] = list(players)

    return jsonify(data)


# TODO REMOVE
@app.route("/clan/<tag>/trophies.json")
@cache.cached(timeout=1000)
def clan_trophies(tag):
    df = Clan.find_by_tag(tag).to_historical_df()[['members', 'clanPoints']].resample('D').mean().dropna()
    return df.to_json(orient='columns', date_format='iso')


def wait_for_job(job_id, wait_time=2):
    start = datetime.now()
    while (datetime.now() - start).total_seconds() < wait_time:
        sleep(0.2)
        try:
            Job.fetch(job_id, connection=redis_connection)
        except NoSuchJobError:
            break
