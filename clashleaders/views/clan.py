from datetime import datetime
from time import sleep

from flask import jsonify, render_template, request
from inflection import camelize
from mongoengine import DoesNotExist
from rq.exceptions import NoSuchJobError
from rq.job import Job

from clashleaders import app, cache, redis_connection
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
