import json
import logging
from codecs import decode, encode
from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON, BYTEA

from clashleaders import db

logger = logging.getLogger(__name__)

IGNORED_ATTRIBUTES = ['clan']


class PlayerModel(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(12), index=True)
    name = db.Column(db.String())
    clan_id = db.Column(db.Integer, db.ForeignKey('clan.id'), nullable=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bytes = db.Column(BYTEA)

    achievements = db.Column(JSON)
    heroes = db.Column(JSON)
    league = db.Column(JSON)
    legendStatistics = db.Column(JSON)
    spells = db.Column(JSON)
    troops = db.Column(JSON)
    attackWins = db.Column(db.Integer)
    bestVersusTrophies = db.Column(db.Integer)
    builderHallLevel = db.Column(db.Integer)
    defenseWins = db.Column(db.Integer)
    donations = db.Column(db.Integer)
    donationsReceived = db.Column(db.Integer)
    expLevel = db.Column(db.Integer)
    role = db.Column(db.String(20))
    townHallLevel = db.Column(db.Integer)
    townHallWeaponLevel = db.Column(db.Integer)
    trophies = db.Column(db.Integer)
    versusBattleWinCount = db.Column(db.Integer)
    versusBattleWins = db.Column(db.Integer)
    versusTrophies = db.Column(db.Integer)
    warStars = db.Column(db.Integer)
    bestTrophies = db.Column(db.Integer)

    def __init__(self, json):
        self.tag = json['tag']
        self.name = json['name']
        self.bytes = zip_data(json)

    @property
    def data(self):
        return unzip_data(self.bytes)


def zip_data(map):
    s = json.dumps(map)
    return encode(s.encode('utf8'), 'zlib')


def unzip_data(b):
    return json.loads(decode(b, 'zlib'))
