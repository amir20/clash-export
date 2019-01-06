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
    clan_id = db.Column(db.Integer, db.ForeignKey('clan.id'), nullable=True, index=True)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    bytes = db.Column(BYTEA)

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
