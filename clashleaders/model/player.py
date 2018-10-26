import json
from codecs import decode, encode
from mongoengine import DynamicDocument, BinaryField, signals, StringField, DictField


class Player(DynamicDocument):
    COMPRESSED_FIELDS = ['achievements', 'clan', 'heroes', 'league', 'legendStatistics', 'spells', 'troops']

    binary_bytes = BinaryField()
    tag = StringField(required=True, unique=True)
    lab_levels = DictField()

    meta = {
        'indexes': [
            'name',
            'tag',
            'townHallWeaponLevel',
            'townHallLevel',
            'trophies',
            'warStars',
            'expLevel',
            'builderHallLevel',
            'defenseWins',
            'attackWins',
            'donations'
        ]
    }

    @classmethod
    def upsert_player(cls, player_tag, **kwargs):
        player = Player.objects(tag=player_tag).first()

        if not player:
            player = Player(**kwargs).save()
        else:
            # This is ugly but update() doesn't trigger pre_save
            for key, value in kwargs.items():
                setattr(player, key, value)
            player.save()

        return player

    @classmethod
    def post_init(cls, sender, document, **kwargs):
        if document.binary_bytes:
            data = decode_data(document.binary_bytes)

            for f in cls.COMPRESSED_FIELDS:
                if f in data:
                    setattr(document, f, data[f])

    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        document.heroes = document.heroes or []
        document.troops = document.troops or []
        document.spells = document.spells or []

        for lab in document.heroes + document.troops + document.spells:
            key = f"{lab['village']}_{lab['name'].replace('.', '')}"
            document.lab_levels[key] = lab['level']

        data = dict()
        for f in cls.COMPRESSED_FIELDS:
            if hasattr(document, f):
                data[f] = getattr(document, f)
                delattr(document, f)

        document.binary_bytes = encode_data(data)


signals.post_init.connect(Player.post_init, sender=Player)
signals.pre_save.connect(Player.pre_save, sender=Player)
signals.post_save.connect(Player.post_init, sender=Player)


def encode_data(map):
    s = json.dumps(map)
    return encode(s.encode('utf8'), 'zlib')


def decode_data(b):
    return json.loads(decode(b, 'zlib'))
