import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler


def cluster_clans(file_or_stream):
    df = pd.read_csv(file_or_stream, index_col='tag')

    scaled_features = MinMaxScaler().fit_transform(df.values)
    scaled_df = pd.DataFrame(scaled_features, index=df.index, columns=df.columns)
    X = scaled_df.as_matrix()
    total, _ = X.shape

    kmeans = KMeans(n_clusters=int(total / 90)).fit(X)
    df['label'] = kmeans.labels_
    return df['label'].to_dict()
