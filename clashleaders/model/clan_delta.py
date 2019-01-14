from mongoengine import EmbeddedDocument, FloatField, IntField


class ClanDelta(EmbeddedDocument):
    avg_donations = FloatField()
    avg_donations_received = FloatField()
    avg_gold_grab = FloatField()
    avg_elixir_grab = FloatField()
    avg_de_grab = FloatField()
    avg_war_stars = FloatField()
    avg_attack_wins = FloatField()
    avg_versus_wins = FloatField()
    total_trophies = IntField()
    total_bh_trophies = IntField()
    total_gold_grab = IntField()
    total_elixir_grab = IntField()
    total_de_grab = IntField()
    total_donations = IntField()
    total_attack_wins = IntField()
    total_versus_wins = IntField()
