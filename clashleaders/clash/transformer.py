from collections import namedtuple
from functools import reduce
from clashleaders import cache
from clashleaders.util import correct_tag

import clashleaders.model.clan

ShortClan = namedtuple("ShortClan", "name tag badge slug members score")


def deep_getattr(obj, attr):
    return reduce(getattr, attr.split("."), obj)


def to_short_clan(clan, prop=None):
    score = None if prop is None else deep_getattr(clan, prop)
    return ShortClan(name=clan.name, tag=clan.tag, badge=clan.badgeUrls.get("small"), members=clan.members, slug=getattr(clan, "slug", None), score=score)


@cache.memoize(timeout=43200)
def tag_to_slug(tag: str) -> str:
    clan = clashleaders.model.clan.Clan.objects(tag=correct_tag(tag)).only("slug").first()
    return clan.slug if clan else None
