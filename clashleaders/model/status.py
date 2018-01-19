from datetime import datetime

from mongoengine import *


class Status(Document):
    last_updated = DateTimeField(default=datetime.now)
    total_clans = IntField()
    total_members = IntField()
    ratio_indexed = FloatField()
