from clashleaders import cache

import clashleaders.model.clan


@cache.memoize(timeout=86400)
def similar_clans_avg(cluster_label: int, column: str) -> float:
    return clashleaders.model.clan.Clan.objects(cluster_label=cluster_label).average(column)
