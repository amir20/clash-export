from clashleaders.clash.transformer import tag_to_slug
import logging
import graphene
from graphene.types.generic import GenericScalar

import clashleaders.graphql.clan as clan
from .badge import BadgeUrls

logger = logging.getLogger(__name__)


class WarClan(graphene.ObjectType):
    name = graphene.String()
    tag = graphene.String()
    slug = graphene.String()
    badge_urls = graphene.Field(BadgeUrls)
    attacks = graphene.Int()
    stars = graphene.Int()
    destruction_percentage = graphene.Float()

    def resolve_slug(parent, info):
        return tag_to_slug(parent.tag)

    def resolve_badge_urls(parent, info):
        return BadgeUrls(**parent.badge_urls)


class War(graphene.ObjectType):
    endTime = graphene.Float()
    startTime = graphene.Float()
    aggregated = GenericScalar()
    state = graphene.String()
    opponent = graphene.Field(WarClan)
    clan = graphene.Field(WarClan)

    def resolve_startTime(parent, info):
        return parent.startTime.timestamp() * 1000

    def resolve_endTime(parent, info):
        return parent.endTime.timestamp() * 1000

    def resolve_opponent(parent, info):
        return WarClan(
            name=parent.opponent["name"],
            tag=parent.opponent["tag"],
            badge_urls=parent.opponent["badgeUrls"],
            attacks=parent.opponent["attacks"],
            stars=parent.opponent["stars"],
            destruction_percentage=parent.opponent["destructionPercentage"],
        )

    def resolve_clan(parent, info):
        return WarClan(
            name=parent.clan["name"],
            tag=parent.clan["tag"],
            badge_urls=parent.clan["badgeUrls"],
            attacks=parent.clan["attacks"],
            stars=parent.clan["stars"],
            destruction_percentage=parent.clan["destructionPercentage"],
        )

    def resolve_aggregated(parent, info):
        df = parent.to_df()
        df = df.drop(
            columns=[
                "attack1.attackerTag",
                "attack1.defenderTag",
                "attack2.attackerTag",
                "attack2.defenderTag",
                "bestOpponentAttack.attackerTag",
                "bestOpponentAttack.defenderTag",
            ],
            errors="ignore",
        )
        df.columns = df.columns.str.replace(".", "__", regex=False)
        return df.fillna("na").reset_index().to_dict(orient="records")


class CWLGroup(graphene.ObjectType):
    state = graphene.String()
    season = graphene.String()
    clans = GenericScalar()
    aggregated = GenericScalar()

    def resolve_aggregated(self, info):
        try:
            df = self.aggregate_stars_and_destruction(self.clan)
            return df.fillna("na").reset_index().to_dict(orient="records")
        except:
            logger.error("Failed to aggregate clan data for {}".format(self.clan), exc_info=True)
            return None
