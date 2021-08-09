from __future__ import annotations
from typing import Optional
from mongoengine import DynamicDocument, signals
from datetime import datetime
from typing import List

from mongoengine.fields import BooleanField, ListField, ReferenceField, StringField
from clashleaders.util import correct_tag, from_timestamp

import pandas as pd


class CWLWar(DynamicDocument):
    war_tag = StringField(required=True, unique=True)

    meta = {
        "index_background": True,
        "indexes": [
            "war_tag",
        ],
    }

    def __repr__(self):
        return "<CWLWar war_tag={} clan={} opponent={}>".format(self.war_tag, self.clan["tag"], self.opponent["tag"])

    def to_df(self) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(self.clan["members"])
        return (
            df.join(df["attacks"].apply(lambda column: pd.Series(column[0])).add_prefix("attack."))
            .join(df["bestOpponentAttack"].apply(lambda column: pd.Series(column)).add_prefix("bestOpponentAttack."))
            .drop(["attacks", "bestOpponentAttack"], axis=1)
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
