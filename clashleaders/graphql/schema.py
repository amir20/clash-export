import logging
from datetime import datetime, timedelta
import graphene
import clashleaders.model as model

from clashleaders.clash import api
from rq.exceptions import NoSuchJobError

from .clan import Clan, ShortClan
from .player import Player
from time import sleep


logger = logging.getLogger(__name__)


class Query(graphene.ObjectType):
    player = graphene.Field(Player, tag=graphene.String(required=True))
    clan = graphene.Field(
        Clan,
        tag=graphene.String(required=True),
        refresh=graphene.Int(required=False),
        update_wars=graphene.Boolean(required=False),
    )
    search_clan = graphene.List(ShortClan, query=graphene.String(required=True))

    def resolve_clan(self, info, tag, refresh=False, update_wars=False):
        if refresh:
            clan = model.Clan.find_by_tag(tag)
            clan.update(inc__page_views=1)
            delta = datetime.now() - clan.updated_on
            if timedelta(minutes=refresh) < delta:
                clan = model.Clan.fetch_and_update(tag, sync_calculation=False)
                wait_for_job(clan.job)

        clan = model.Clan.find_by_tag(tag)
        if update_wars:
            clan.update_wars()

        return clan

    def resolve_player(self, info, tag):
        return model.Player.find_by_tag(tag)

    def resolve_search_clan(self, info, query):
        try:
            clan = api.find_clan_by_tag(query)
            results = [model.Clan(**clan)]
        except api.ClanNotFound:
            results = [model.Clan(**c) for c in api.search_by_name(query, limit=6)]

        tags = [c.tag for c in results]
        existing_clans = list(model.Clan.objects(tag__in=tags))
        slugs = {c.tag: c.slug for c in existing_clans}

        for c in results:
            c.slug = slugs.get(c.tag)

        return results


def wait_for_job(job, wait_time=3):
    start = datetime.now()
    while (datetime.now() - start).total_seconds() < wait_time:
        sleep(0.2)
        try:
            job.refresh()
        except NoSuchJobError:
            break
