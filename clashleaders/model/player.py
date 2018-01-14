from mongoengine import *


class Player(DynamicDocument):
    meta = {
        'indexes': [
            'clan.name',
            'clan.tag',
            'name',
            'tag'
        ]
    }
