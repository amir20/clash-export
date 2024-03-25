import logging
import os

from clashleaders.clustering.csv_export import clans_to_csv
from clashleaders.clustering.kmeans import train_model
from clashleaders.model import Clan

logger = logging.getLogger(__name__)


def compute_similar_clans():
    filename = "/tmp/clans.csv"

    logger.info("Writing clans to csv file.")
    with open(filename, "w") as f:
        clans_to_csv(f)

    logger.info("Computing kmeans for clans and saving model.")
    labels = train_model(filename)

    os.remove(filename)

    logger.info(f"Updating labels for {len(labels)} clans.")
    for tag, label in labels.items():
        Clan.objects(tag=tag).update_one(set__cluster_label=label)
