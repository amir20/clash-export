from mongoengine import EmbeddedDocument, FloatField, IntField


class ClanDelta(EmbeddedDocument):
    avg_donations = FloatField(required=True)
    avg_donations_received = FloatField(required=True)
    avg_gold_grab = FloatField(required=True)
    avg_elixir_grab = FloatField(required=True)
    avg_de_grab = FloatField(required=True)
    avg_war_stars = FloatField(required=True)
    avg_attack_wins = FloatField(required=True)
    avg_versus_wins = FloatField(required=True)
    total_trophies = IntField()
    total_bh_trophies = IntField()
    total_gold_grab = IntField()
    total_elixir_grab = IntField()
    total_de_grab = IntField()
    total_donations = IntField()
    total_attack_wins = IntField()
    total_versus_wins = IntField()
