import pandas as pd

from .transformer import transform_players


def compare(now, then):
    now_df = to_data_frame(now)
    then_df = to_data_frame(then)
    delta = now_df.drop(columns='Tag') - then_df.drop(columns='Tag')
    return delta['Total Gold Grab'].mean()


def to_data_frame(clan):
    tf = transform_players(clan.players)
    df = pd.DataFrame(data=tf, columns=tf[0])
    df = df.set_index('Name')
    df = df.iloc[1:]
    return df
