import pandas as pd

from model import ClanPreCalculated, ClanDelta
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

    calculate_avg(cpc)
    calculate_season(cpc)

    cpc.save()


def calculate_avg(cpc):
    df = to_data_frame(cpc.most_recent)

    cpc.avg_donations = df['Total Donations'].mean()

    cpc.avg_gold_grab = df['Total Gold Grab'].mean()
    cpc.avg_elixir_grab = df['Total Elixir Grab'].mean()
    cpc.avg_de_grab = df['Total DE Grab'].mean()
    cpc.avg_war_stars = df['Total War Stars'].mean()

    cpc.avg_th_level = df['TH Level'].mean()
    cpc.avg_bh_level = df['BH Level'].mean()
    cpc.avg_xp_level = df['XP Level'].mean()
    cpc.avg_best_trophies = df['Best Trophies'].mean()
    cpc.avg_trophies = df['Current Trophies'].mean()
    cpc.avg_bh_trophies = df['Builder Hall Trophies'].mean()


def calculate_season(cpc):
    start_df = to_data_frame(cpc.season_start)
    now_df = to_data_frame(cpc.most_recent)

    season_delta = calculate_delta(now_df, start_df)

    cpc.season_delta = season_delta


def calculate_delta(now_df, start_df):
    avg_donations = now_df['Donations'].mean()
    avg_donations_received = now_df['Donations Received'].mean()

    avg_gold_grab = avg_column('Total Gold Grab', now_df, start_df)
    avg_elixir_grab = avg_column('Total Elixir Grab', now_df, start_df)
    avg_de_grab = avg_column('Total DE Grab', now_df, start_df)
    avg_war_stars = avg_column('Total War Stars', now_df, start_df)

    avg_th_level = avg_column('TH Level', now_df, start_df)
    avg_bh_level = avg_column('BH Level', now_df, start_df)
    avg_xp_level = avg_column('XP Level', now_df, start_df)
    avg_best_trophies = avg_column('Best Trophies', now_df, start_df)
    avg_trophies = avg_column('Current Trophies', now_df, start_df)
    avg_bh_trophies = avg_column('Builder Hall Trophies', now_df, start_df)

    return ClanDelta(
        avg_donations=avg_donations,
        avg_donations_received=avg_donations_received,
        avg_gold_grab=avg_gold_grab,
        avg_elixir_grab=avg_elixir_grab,
        avg_de_grab=avg_de_grab,
        avg_war_stars=avg_war_stars,
        avg_th_level=avg_th_level,
        avg_bh_level=avg_bh_level,
        avg_xp_level=avg_xp_level,
        avg_best_trophies=avg_best_trophies,
        avg_trophies=avg_trophies,
        avg_bh_trophies=avg_bh_trophies
    )


def avg_column(column, now, start):
    return (now[column] - start[column]).mean()


def is_new_season(before, now):
    before_df = to_data_frame(before)
    now_df = to_data_frame(now)

    before_donations = before_df['Donations']
    now_donations = now_df['Donations']

    intersection = before_donations.index.intersection(now_donations.index)

    return (before_donations[intersection] > now_donations[intersection]).all()


def to_data_frame(clan):
    tf = transform_players(clan.players)
    df = pd.DataFrame(data=tf, columns=tf[0])
    df = df.set_index('Name')
    df = df.iloc[1:]
    return df
