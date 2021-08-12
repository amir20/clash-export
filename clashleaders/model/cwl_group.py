from __future__ import annotations
from clashleaders.model.cwl_war import CWLWar
from typing import Optional
from mongoengine import DynamicDocument
from datetime import datetime
from typing import List

from mongoengine.fields import BooleanField, ListField, ReferenceField, StringField
from clashleaders.util import correct_tag, from_timestamp


class CWLGroup(DynamicDocument):
    round_wars = ListField(ReferenceField(CWLWar))

    meta = {
        "index_background": True,
        "indexes": [
            ("clans.tag", "season"),
        ],
    }

    def __repr__(self):
        return "<CWLGroup season={}>".format(self.season)

    @classmethod
    def find_by_clan_and_season(cls, tag: str, season: str) -> Optional[CWLGroup]:
        tag = correct_tag(tag)
        return cls.objects(clans__tag=tag, season=season).first()