from __future__ import annotations
from typing import Optional
from mongoengine import DynamicDocument, StringField


class War(DynamicDocument):

    meta = {
        "index_background": True,
        "indexes": ["clan.tag", "members.tag"],
    }

    def __repr__(self):
        return "<War clan={0}>".format(self.clan["tag"])
