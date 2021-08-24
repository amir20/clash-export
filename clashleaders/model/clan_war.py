from __future__ import annotations
from typing import Optional
from mongoengine import DynamicDocument, signals
from datetime import datetime
from typing import List

from mongoengine.fields import BooleanField, ListField, ReferenceField, StringField
from clashleaders.util import correct_tag, from_timestamp

import pandas as pd


class ClanWar(DynamicDocument):
    meta = {
        "index_background": True,
        "indexes": [
            "clan.tag",
            "members.tag",
            "preparationStartTime",
            "startTime",
            "endTime",
            ("clan.tag", "startTime"),
        ],
    }

    def __repr__(self):
        return "<ClanWar clan={} opponent={}>".format(self.clan["tag"], self.opponent["tag"])

    def to_df(self) -> pd.DataFrame:
        members = self.clan["members"]
        for member in members:
            if "attacks" not in member:
                member["attacks"] = []
            member["attack_1"] = member["attacks"][0] if len(member["attacks"]) > 0 else None
            member["attack_2"] = member["attacks"][1] if len(member["attacks"]) > 1 else None

        df = pd.json_normalize(members).drop(columns=["attacks", "attack_2", "attack_1"], errors="ignore").set_index("tag")

        return df

    @classmethod
    def init(cls, sender, document, **kwargs):
        document.preparationStartTime = from_timestamp(document.preparationStartTime)
        document.startTime = from_timestamp(document.startTime)
        document.endTime = from_timestamp(document.endTime)

    @classmethod
    def find_by_clan_and_start_time(cls, tag: str, start_time: datetime) -> Optional[ClanWar]:
        tag = correct_tag(tag)
        return cls.objects(clan__tag=tag, startTime=start_time).first()


signals.post_init.connect(ClanWar.init, sender=ClanWar)
signals.pre_save.connect(ClanWar.init, sender=ClanWar)
