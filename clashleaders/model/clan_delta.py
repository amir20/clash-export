from mongoengine import EmbeddedDocument, FloatField, IntField


class ClanDelta(EmbeddedDocument):
    avg_donations = FloatField(default=0)
    avg_donations_received = FloatField(default=0)
    avg_gold_grab = FloatField(default=0)
    avg_elixir_grab = FloatField(default=0)
    avg_de_grab = FloatField(default=0)
    avg_war_stars = FloatField(default=0)
    avg_attack_wins = FloatField(default=0)
    avg_versus_wins = FloatField(default=0)
    total_trophies = IntField(default=0)
    total_bh_trophies = IntField(default=0)
    total_gold_grab = IntField(default=0)
    total_elixir_grab = IntField(default=0)
    total_de_grab = IntField(default=0)
    total_donations = IntField(default=0)
    total_attack_wins = IntField(default=0)
    total_versus_wins = IntField(default=0)
