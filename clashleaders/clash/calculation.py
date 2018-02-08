from datetime import datetime

import numpy as np
import pandas as pd
from mongoengine.errors import DoesNotExist
from slugify import slugify

import clashleaders.model
from .transformer import transform_players


def update_calculations(clan):
    """
    Calculates averages for current, season and last week. If pre calculation doesn't exist
    then one is created.
    :param clan:
    :return:
    """
    cpc = clashleaders.model.ClanPreCalculated.objects(tag=clan.tag).first()
    if cpc is None:
        cpc = clashleaders.model.ClanPreCalculated(tag=clan.tag)
        cpc.season_start = clan
        cpc.most_recent = clan

    try:
        cpc.most_recent
    except DoesNotExist:
        cpc.most_recent = clan

    try:
        cpc.season_start
    except DoesNotExist:
        cpc.season_start = clan

    cpc.name = clan.name
    cpc.clanLevel = clan.clanLevel
    cpc.slug = slugify(f"{clan.name}-{clan.tag}", to_lower=True)
    cpc.description = clan.description
    cpc.members = clan.members
    cpc.clanPoints = clan.clanPoints
    cpc.clanVersusPoints = clan.clanVersusPoints
    cpc.badgeUrls = clan.badgeUrls
    cpc.location = getattr(clan, 'location', {})
    cpc.isWarLogPublic = clan.isWarLogPublic

    cpc.warWinStreak = getattr(clan, 'warWinStreak', 0)
    cpc.warWins = getattr(clan, 'warWins', 0)
    cpc.warTies = getattr(clan, 'warTies', 0)
    cpc.warLosses = getattr(clan, 'warLosses', 0)

    cpc.last_updated = datetime.now

    if is_new_season(cpc.most_recent, clan):
        cpc.season_start = clan

    cpc.most_recent = clan

    calculate_data(cpc)
    calculate_season(cpc)
    calculate_week(cpc)

    cpc.save()

    return cpc


def calculate_data(cpc):
    """
    Calculate all averages for clans based on total values

    :param cpc:
    :return:
    """
    df = to_data_frame(cpc.most_recent)

    cpc.avg_donations = mean_single_column('Donations', df)

    cpc.avg_gold_grab = mean_single_column('Total Gold Grab', df)
    cpc.avg_elixir_grab = mean_single_column('Total Elixir Grab', df)
    cpc.avg_de_grab = mean_single_column('Total DE Grab', df)
    cpc.avg_war_stars = mean_single_column('Total War Stars', df)

    cpc.avg_th_level = mean_single_column('TH Level', df)
    cpc.avg_bh_level = mean_single_column('BH Level', df)
    cpc.avg_xp_level = mean_single_column('XP Level', df)
    cpc.avg_xp_level = mean_single_column('XP Level', df)
    cpc.avg_bk_level = mean_single_column('Barbarian King', df)
    cpc.avg_aq_level = mean_single_column('Archer Queen', df)
    cpc.avg_gw_level = mean_single_column('Grand Warden', df)
    cpc.avg_bm_level = mean_single_column('Battle Machine', df)

    cpc.avg_best_trophies = mean_single_column('Best Trophies', df)
    cpc.avg_trophies = mean_single_column('Current Trophies', df)
    cpc.avg_bh_trophies = mean_single_column('Builder Hall Trophies', df)

    cpc.avg_attack_wins = mean_single_column('Attack Wins', df)
    cpc.avg_versus_wins = mean_single_column('Versus Battle Wins', df)

    cpc.total_donations = sum_single_column('Donations', df)
    cpc.total_attack_wins = sum_single_column('Attack Wins', df)
    cpc.total_versus_wins = sum_single_column('Versus Battle Wins', df)


def sum_single_column(column, df):
    value = df[column].sum()
    return 0 if np.isnan(value) else value


def mean_single_column(column, df):
    value = df[column].mean()
    return 0 if np.isnan(value) else value


def calculate_week(cpc):
    """
    Calculates last weeks averages
    :param cpc:
    :return:
    """
    start_df = to_data_frame(clashleaders.model.Clan.from_now_with_tag(cpc.tag, days=7).first())
    now_df = to_data_frame(cpc.most_recent)

    cpc.week_delta = calculate_delta(now_df, start_df)


def calculate_season(cpc):
    """
    Calculates season averages based on season_start
    :param cpc:
    :return:
    """
    start_df = to_data_frame(cpc.season_start)
    now_df = to_data_frame(cpc.most_recent)

    cpc.season_delta = calculate_delta(now_df, start_df)


def calculate_delta(now_df, start_df):
    avg_donations = avg_column('Total Donations', now_df, start_df)
    avg_donations_received = avg_column('Donations Received', now_df, start_df)

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

    avg_attack_wins = avg_column('Attack Wins', now_df, start_df)
    avg_versus_wins = avg_column('Versus Battle Wins', now_df, start_df)

    total_trophies = sum_column('Current Trophies', now_df, start_df)
    total_bh_trophies = sum_column('Builder Hall Trophies', now_df, start_df)
    total_gold_grab = sum_column('Total Gold Grab', now_df, start_df)
    total_elixir_grab = sum_column('Total Elixir Grab', now_df, start_df)
    total_de_grab = sum_column('Total DE Grab', now_df, start_df)
    total_donations = sum_column('Total Donations', now_df, start_df)
    total_attack_wins = sum_column('Attack Wins', now_df, start_df)
    total_versus_wins = sum_column('Versus Battle Wins', now_df, start_df)

    return clashleaders.model.ClanDelta(
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
        avg_bh_trophies=avg_bh_trophies,
        avg_attack_wins=avg_attack_wins,
        avg_versus_wins=avg_versus_wins,
        total_trophies=total_trophies,
        total_bh_trophies=total_bh_trophies,
        total_gold_grab=total_gold_grab,
        total_elixir_grab=total_elixir_grab,
        total_de_grab=total_de_grab,
        total_donations=total_donations,
        total_attack_wins=total_attack_wins,
        total_versus_wins=total_versus_wins
    )


def avg_column(column, now, start):
    value = (now[column] - start[column]).mean()
    return 0 if np.isnan(value) else value


def sum_column(column, now, start):
    value = (now[column] - start[column]).sum()
    return 0 if np.isnan(value) else value


def is_new_season(before, now):
    """
    Calculates season start based on donations
    :param before:
    :param now:
    :return:
    """
    before_df = to_data_frame(before)
    now_df = to_data_frame(now)

    before_donations = before_df['Donations']
    now_donations = now_df['Donations']

    return before_donations.gt(now_donations).any()


def to_data_frame(clan):
    tf = transform_players(clan.players)
    df = pd.DataFrame(data=tf, columns=tf[0])
    df = df.set_index('Tag')
    df = df.iloc[1:]
    return df
