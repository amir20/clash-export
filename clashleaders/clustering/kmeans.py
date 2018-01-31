import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans


def cluster_clans(file_or_stream):
    df = pd.read_csv(file_or_stream, index_col=0, names=['tag', 'members', 'week_trophies', 'week_bh_trophies', 'week_total_donations',
                                                         'week_attacks_wins', 'week_versus_wins', 'week_gold_grab', 'week_avg_war_stars'])

    scaled_features = MinMaxScaler().fit_transform(df.values)
    scaled_df = pd.DataFrame(scaled_features, index=df.index, columns=df.columns)
    X = scaled_df.as_matrix()
    total, _ = X.shape

    kmeans = KMeans(n_clusters=int(total / 90)).fit(X)
    df['label'] = kmeans.labels_
    return df['label'].to_dict()
