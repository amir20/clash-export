from __future__ import annotations

from typing import List, TYPE_CHECKING
from mongoengine import DynamicDocument, signals

from mongoengine.fields import StringField
from clashleaders.util import correct_tag, from_timestamp

import pandas as pd

if TYPE_CHECKING:
    from clashleaders.model.clan import Clan


class CWLWar(DynamicDocument):
    war_tag = StringField(required=True, unique=True)

    meta = {
        "index_background": True,
        "indexes": [
            "war_tag",
            "clan.members.tag",
            "opponent.members.tag",
            "endTime",
        ],
    }

    def __repr__(self):
        return "<CWLWar war_tag={} clan={} opponent={}>".format(self.war_tag, self.clan["tag"], self.opponent["tag"])

    def contains_clan(self, clan: Clan) -> bool:
        return clan.tag in (self.clan["tag"], self.opponent["tag"])

    def to_df(self, clan: Clan) -> pd.DataFrame:
        if not self.contains_clan(clan):
            raise ValueError("Clan not found")

        members = None
        if self.clan["tag"] == clan.tag:
            members = self.clan["members"]
        else:
            members = self.opponent["members"]

        df = pd.json_normalize(members)
        return (
            df.join(df["attacks"].apply(lambda col: pd.Series(col[0]) if pd.notnull(col) else pd.Series(dtype=object)).add_prefix("attack."))
            .drop(["attacks"], axis=1)
            .set_index("tag")
        )

    @classmethod
    def init(cls, sender, document, **kwargs):
        document.preparationStartTime = from_timestamp(document.preparationStartTime)
        document.startTime = from_timestamp(document.startTime)
        document.endTime = from_timestamp(document.endTime)

    @classmethod
    def find_by_war_tags(cls, war_tags) -> List[CWLWar]:
        return cls.objects(war_tag__in=war_tags)


signals.post_init.connect(CWLWar.init, sender=CWLWar)
signals.pre_save.connect(CWLWar.init, sender=CWLWar)
