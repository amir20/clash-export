from __future__ import annotations
from typing import Optional
from mongoengine import DynamicDocument, signals
from datetime import datetime
from clashleaders.util import correct_tag, from_timestamp


class War(DynamicDocument):

    meta = {
        "index_background": True,
        "indexes": [
            "clan.tag",
            "members.tag",
            "preparationStartTime",
            "startTime",
            "endTime",
            ("clan.tag", "startTime"),
            ("clan.tag", "season"),
            ("clans.tag", "season"),
        ],
    }

    def __repr__(self):
        if self.is_cwl:
            return "<War clan={} season={} is_cwl=true>".format(self.clan["tag"], self.season)
        else:
            return "<War clan={}>".format(self.clan["tag"])

    @classmethod
    def init(cls, sender, document, **kwargs):
        document.is_cwl = "season" in document
        if "preparationStartTime" in document:
            document.preparationStartTime = from_timestamp(document.preparationStartTime)
            document.startTime = from_timestamp(document.startTime)
            document.endTime = from_timestamp(document.endTime)

    @classmethod
    def find_by_clan_and_start_time(cls, tag: str, start_time: datetime) -> Optional[War]:
        tag = correct_tag(tag)
        return cls.objects(clan__tag=tag, startTime=start_time).first()

    @classmethod
    def find_by_clan_and_season(cls, tag: str, season: str) -> Optional[War]:
        tag = correct_tag(tag)
        return cls.objects(clan__tag=tag, season=season).first()


signals.post_init.connect(War.init, sender=War)
signals.pre_save.connect(War.init, sender=War)
