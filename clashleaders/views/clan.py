from flask import render_template
from mongoengine import DoesNotExist

from clashleaders import app, cache
from clashleaders.model import Clan, Status
from clashleaders.text.clan_description_processor import transform_description


@app.context_processor
def inject_most_popular():
    status = Status.instance()
    return dict(status=status, popular_countries=status.top_countries, reddit_clans=status.reddit_clans)


@app.route("/clan/<slug>")
def clan_detail_page(slug):
    try:
        clan = Clan.find_by_slug(slug)
        initial_state = dict(
            name=clan.name,
            tag=clan.tag,
            updatedOn=clan.updated_on.timestamp() * 1000,
            historicData=clan.historical_near_days_ago(7).to_matrix(),
            recentData=clan.historical_near_now().to_matrix(),
            playerStatus={},
            delta=clan.week_delta.to_dict(camel_case=True),
            similar=clan.week_delta.to_dict(camel_case=True),
            oldestDays=clan.days_of_history(),
            trophyHistory=clan.trophy_history(),
        )
    except DoesNotExist:
        return render_template("404.html"), 404
    else:
        return render_template(
            "clan.html",
            clan=clan,
            initial_state=initial_state,
        )
