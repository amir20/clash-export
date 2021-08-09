import clashleaders.model


def aggregate_cwl_activity(war: clashleaders.model.CWLGroup, clan: clashleaders.model.Clan):
    wars = [w for w in war.round_wars if w.opponent["tag"] == clan.tag or w.clan["tag"] == clan.tag]
    pass
