from datetime import datetime

from clashleaders import db


class ClanModel(db.Model):
    __tablename__ = 'clan'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(12), index=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    points = db.Column(db.Integer)
    versusPoints = db.Column(db.Integer)
    members = db.Column(db.Integer)
    players = db.relationship('PlayerModel', backref='player', lazy=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, tag, name, description, points, versusPoints, players):
        self.tag = tag
        self.name = name
        self.description = description
        self.points = points
        self.versusPoints = versusPoints
        self.players = players
        self.members = len(players)

    def __repr__(self):
        return '<Clan {}>'.format(self.tag)
