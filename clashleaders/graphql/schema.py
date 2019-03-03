from graphene import ObjectType, String, Field

from clashleaders.model.player import Player


class PlayerType(ObjectType):
    name = String()
    role = String()
    slug = String()


class Query(ObjectType):
    players = Field(PlayerType, tag=String(required=True))

    def resolve_players(self, info, tag):
        print(info)
        print(tag)
        return Player.find_by_tag(tag)
