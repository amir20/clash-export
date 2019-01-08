from datetime import datetime

from mongoengine import Document, StringField, IntField, DictField, \
    BooleanField, DateTimeField, ReferenceField, ListField

from clashleaders.model.historical_player import HistoricalPlayer


class HistoricalClan(Document):
    created_on = DateTimeField(default=datetime.now)
    tag = StringField(required=True)
    name = StringField(required=True)
    clanLevel = IntField()
    description = StringField()
    clanPoints = IntField()
    clanVersusPoints = IntField()
    members = IntField()
    warWinStreak = IntField()
    warWins = IntField()
    warTies = IntField()
    warLosses = IntField()
    isWarLogPublic = BooleanField()

    badgeUrls = DictField()
    location = DictField()

    players = ListField(ReferenceField(HistoricalPlayer))

    meta = {
        'index_background': True,
        'indexes': [
            'tag',
            ('tag', 'created_on'),
            'members'
        ]
    }

    def __init__(self, *args, **kwargs):
        values = {k: v for k, v in kwargs.items() if k in self._fields_ordered}
        super().__init__(*args, **values)
