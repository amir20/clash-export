from datetime import datetime

import pandas as pd
from cachetools import TTLCache, cached
from sklearn.cluster import MiniBatchKMeans
from sklearn.preprocessing import MinMaxScaler

import clashleaders.model

from .csv_export import extract_features

SCALER = "SCALER_CLUSTER"
KMEANS = "KMEANS_CLUSTER"


def train_model(file_or_stream):
    df = pd.read_csv(file_or_stream, index_col="tag")

    scaler = MinMaxScaler().fit(df.values)
    scaled_features = scaler.transform(df.values)
    scaled_df = pd.DataFrame(scaled_features, index=df.index, columns=df.columns)
    X = scaled_df.values
    total, _ = X.shape

    kmeans = MiniBatchKMeans(n_clusters=int(total / 90), batch_size=20000).fit(X)

    __save_model(SCALER, scaler)
    __save_model(KMEANS, kmeans)

    df["label"] = kmeans.labels_
    return df["label"].to_dict()


def predict_clans(*clans: "clashleaders.model.Clan"):
    scaler = __load_model(SCALER)
    kmeans = __load_model(KMEANS)
    features = [extract_features(clan) for clan in clans]
    transformed = scaler.transform(features)

    return kmeans.predict(transformed).tolist()


def __save_model(name, model):
    trained_model = clashleaders.model.TrainedModel.objects(
        name=name
    ).first() or clashleaders.model.TrainedModel(name=name)
    trained_model.last_updated = datetime.now()
    trained_model.model = model
    trained_model.save()


@cached(cache=TTLCache(maxsize=2, ttl=600))
def __load_model(name):
    return clashleaders.model.TrainedModel.objects.get(name=name).model
