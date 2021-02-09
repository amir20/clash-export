import clashleaders.views
from flask import render_template
from mongoengine import DoesNotExist

from clashleaders import app
from clashleaders.model import Clan, Status


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
            clanPoints=clan.clanPoints,
            clanVersusPoints=clan.clanVersusPoints,
            weekDelta=clan.week_delta.to_dict(camel_case=True),
            monthDelta=clan.month_delta.to_dict(camel_case=True),
            computed=clan.computed.to_dict(camel_case=True),
            updatedOn=clan.updated_on.timestamp() * 1000,
            historicData=clan.historical_near_days_ago(7).to_matrix(),
            recentData=clan.historical_near_now().to_matrix(),
            playerStatus={},
            location=clan.location,
            members=clan.members,
            clanLevel=clan.clanLevel,
            delta=clan.week_delta.to_dict(camel_case=True),
            similar=clan.week_delta.to_dict(camel_case=True),
            oldestDays=clan.days_of_history(),
            badgeUrls=dict(large=clashleaders.views.imgproxy_url(clan.badgeUrls["large"])),
            richDescription=clan.rich_description,
            trophyHistory=clan.trophy_history(),
            verifiedAccounts=clan.verified_accounts,
            labels=labels(clan),
            warLeague=clan.warLeague,
        )
    except DoesNotExist:
        return render_template("404.html"), 404
    else:
        return render_template(
            "clan.html",
            clan=clan,
            initial_state=initial_state,
        )


def labels(clan):
    labels = clan.labels
    for label in labels:
        label["iconUrls"] = {key: clashleaders.views.imgproxy_url(value) for key, value in label["iconUrls"].items()}

    return labels
