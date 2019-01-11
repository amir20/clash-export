from datetime import datetime, timedelta

import numpy as np

from clashleaders.model.clan_delta import ClanDelta


def update_calculations(clan):
    last_week = clan.historical_near_time(dt=datetime.now() - timedelta(days=7))
    most_recent = clan.historical_near_now()
    most_recent_df = most_recent.to_df()

    clan.computed = calculate_data(most_recent_df)
    clan.week_delta = calculate_delta(start_df=last_week.to_df(), now_df=most_recent_df)

    # if cpc.cluster_label == -1:
    #     [label] = predict_clans(cpc)
    #     cpc.cluster_label = label

    clan.save()


def calculate_data(df):
    return ClanDelta(
        avg_donations=mean_single_column('Donations', df),
        avg_donations_received=mean_single_column('Donations Received', df),
        avg_gold_grab=mean_single_column('Total Gold Grab', df),
        avg_elixir_grab=mean_single_column('Total Elixir Grab', df),
        avg_de_grab=mean_single_column('Total DE Grab', df),
        avg_war_stars=mean_single_column('Total War Stars', df),
        avg_attack_wins=mean_single_column('Attack Wins', df),
        avg_versus_wins=mean_single_column('Builder Hall Trophies', df),
        total_donations=sum_single_column('Donations', df),
        total_gold_grab=sum_single_column('Total Gold Grab', df),
        total_elixir_grab=sum_single_column('Total Elixir Grab', df),
        total_de_grab=sum_single_column('Total DE Grab', df),
        total_attack_wins=sum_single_column('Attack Wins', df),
        total_versus_wins=sum_single_column('Versus Battle Wins', df)
    )


def calculate_delta(now_df, start_df):
    return ClanDelta(
        avg_donations=avg_column('Total Donations', now_df, start_df),
        avg_donations_received=avg_column('Donations Received', now_df, start_df),
        avg_gold_grab=avg_column('Total Gold Grab', now_df, start_df),
        avg_elixir_grab=avg_column('Total Elixir Grab', now_df, start_df),
        avg_de_grab=avg_column('Total DE Grab', now_df, start_df),
        avg_war_stars=avg_column('Total War Stars', now_df, start_df),
        avg_attack_wins=avg_column('Attack Wins', now_df, start_df),
        avg_versus_wins=avg_column('Versus Battle Wins', now_df, start_df),
        total_trophies=sum_column('Current Trophies', now_df, start_df),
        total_bh_trophies=sum_column('Builder Hall Trophies', now_df, start_df),
        total_gold_grab=sum_column('Total Gold Grab', now_df, start_df),
        total_elixir_grab=sum_column('Total Elixir Grab', now_df, start_df),
        total_de_grab=sum_column('Total DE Grab', now_df, start_df),
        total_donations=sum_column('Total Donations', now_df, start_df),
        total_attack_wins=sum_column('Attack Wins', now_df, start_df),
        total_versus_wins=sum_column('Versus Battle Wins', now_df, start_df),
    )


def avg_column(column, now, start):
    value = (now[column] - start[column]).mean()
    return 0 if np.isnan(value) else value


def sum_column(column, now, start):
    value = (now[column] - start[column]).sum()
    return 0 if np.isnan(value) else value


def sum_single_column(column, df):
    value = df[column].sum()
    return 0 if np.isnan(value) else value


def mean_single_column(column, df):
    value = df[column].mean()
    return 0 if np.isnan(value) else value
