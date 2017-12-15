import pandas as pd

from .transformer import transform_players


def update_calculations(clan):
    cpc = ClanPreCalculated.objects(tag=clan.tag).first()
    if cpc is None:
        cpc = ClanPreCalculated(tag=clan.tag)
        cpc.season_start = clan
        cpc.most_recent = clan

    cpc.name = clan.name
    cpc.description = clan.description
    cpc.members = clan.members
    cpc.clanPoints = clan.clanPoints
    cpc.clanVersusPoints = clan.clanVersusPoints

    if is_new_season(cpc.most_recent, clan):
        cpc.season_start = clan

    cpc.most_recent = clan

    cpc.save()
    

def is_new_season(before, now):
    before_df = to_data_frame(before)
    now_df = to_data_frame(now)

    before_donations = before_df['Donations']
    now_donations = now_df['Donations']

    intersection = before_donations.index.intersection(now_donations.index)

    return (before_donations[intersection] > now_donations[intersection]).any()


def to_data_frame(clan):
    tf = transform_players(clan.players)
    df = pd.DataFrame(data=tf, columns=tf[0])
    df = df.set_index('Name')
    df = df.iloc[1:]
    return df
