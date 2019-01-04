from datetime import datetime

from sqlalchemy.dialects.postgresql import JSON

from clashleaders import db


class PlayerModel(db.Model):
    __tablename__ = 'player'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(12), index=True)
    name = db.Column(db.String())
    clan_id = db.Column(db.Integer, db.ForeignKey('clan.id'), nullable=True)
    data = db.Column(JSON)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, json):
        self.tag = json['tag']
        self.name = json['name']
        self.data = json

    def __repr__(self):
        return '<Player {}>'.format(self.tag)
