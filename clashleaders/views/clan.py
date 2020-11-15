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
        description = transform_description(clan.description)
        initial_state = dict(
            name=clan.name,
            tag=clan.tag,
            updatedOn=clan.updated_on.timestamp() * 1000,
            historicData=historical_players_week(clan),
            recentData=historical_players_now(clan),
            playerStatus={},
            delta=clan.week_delta.to_dict(camel_case=True),
            similar=clan.week_delta.to_dict(camel_case=True),
            oldestDays=days_of_history(clan),
        )
    except DoesNotExist:
        return render_template("404.html"), 404
    else:
        return render_template(
            "clan.html",
            clan=clan,
            trophy_distribution=clan_trophies(clan),
            initial_state=initial_state,
            description=description,
        )


@cache.memoize(600)
def clan_trophies(clan):
    df = clan.to_historical_df()[["members", "clanPoints"]].resample("D").mean().dropna()
    df = df.reset_index().rename(columns={"created_on": "labels"})
    df["labels"] = df["labels"].dt.strftime("%Y-%m-%dT%H:%M:%S+00:00Z")
    return df.to_dict("list")


@cache.memoize(1000)
def historical_players_week(clan):
    return clan.historical_near_days_ago(7).to_matrix()


@cache.memoize(120)
def historical_players_now(clan):
    return clan.historical_near_now().to_matrix()


@cache.memoize(1000)
def days_of_history(clan):
    return clan.days_of_history()
