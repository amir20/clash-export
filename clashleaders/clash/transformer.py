from collections import namedtuple
from functools import reduce

ShortClan = namedtuple("ShortClan", "name tag badge slug members score")


def deep_getattr(obj, attr):
    return reduce(getattr, attr.split("."), obj)


def to_short_clan(clan, prop=None):
    score = None if prop is None else deep_getattr(clan, prop)
    return ShortClan(name=clan.name, tag=clan.tag, badge=clan.badgeUrls.get("small"), members=clan.members, slug=getattr(clan, "slug", None), score=score)
