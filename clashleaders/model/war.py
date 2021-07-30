from __future__ import annotations
from typing import Optional
from mongoengine import DynamicDocument, StringField
from datetime import datetime
from clashleaders.util import correct_tag, from_timestamp


class War(DynamicDocument):

    meta = {
        "index_background": True,
        "indexes": ["clan.tag", "members.tag", "preparationStartTime", "startTime", "endTime"],
    }

    def __init__(self, *args, **kwargs):

        kwargs["preparationStartTime"] = from_timestamp(kwargs.get("preparationStartTime"))
        kwargs["startTime"] = from_timestamp(kwargs.get("startTime"))
        kwargs["endTime"] = from_timestamp(kwargs.get("endTime"))
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return "<War clan={0}>".format(self.clan["tag"])

    @classmethod
    def find_by_clan_and_start_time(cls, tag: str, start_time: datetime) -> Optional[War]:
        tag = correct_tag(tag)
        return cls.objects(clan__tag=tag, startTime=start_time).first()
