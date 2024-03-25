from clashleaders.model import *
from datetime import datetime, timedelta
import pandas as pd

last_week = datetime.now() - timedelta(days=7)
tags = HistoricalClan.objects(warLeagueId=48000017, created_on__lte=last_week).distinct(
    "tag"
)
last_day = datetime.now() - timedelta(days=1)
dropped = HistoricalClan.objects(
    warLeagueId=48000016, created_on__gte=last_day, tag__in=tags
).distinct("tag")


clans = [Clan.find_by_tag(tag) for tag in dropped]

frames = [
    clan.cwl_wars().first().aggregate_stars_and_destruction(clan) for clan in clans
]

data = pd.concat(frames)

df = data[data["stars_avg"] > 2.5]
