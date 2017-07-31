from mongoengine import DynamicDocument


class Player(DynamicDocument):
    meta = {
        'indexes': [
            'clan.name',
            'clan.tag',
            'name',
            'tag'
        ]
    }
    

class Clan(DynamicDocument):
    meta = {
        'indexes': [
            'name',
            'tag'
        ]
    }
    
