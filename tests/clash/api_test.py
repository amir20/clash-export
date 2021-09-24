import pytest
from aioresponses import aioresponses

from clashleaders.clash import api


def test_find_clan_bad():
    with aioresponses() as m:
        m.get(
            "https://api.clashofclans.com/v1/clans/%23ABC",
            status=500,
            headers={"Cache-Control": "max-age=60"},
        )

        with pytest.raises(api.ApiException):
            api.find_clan_by_tag("ABC")


def test_find_clan_not_found():
    with aioresponses() as m:
        m.get(
            "https://api.clashofclans.com/v1/clans/%23ABC",
            status=404,
            headers={"Cache-Control": "max-age=60"},
        )

        with pytest.raises(api.ClanNotFound):
            api.find_clan_by_tag("ABC")


def test_find_clan_success():
    with aioresponses() as m:
        p = dict(tag="#ABC")
        m.get(
            "https://api.clashofclans.com/v1/clans/%23ABC",
            status=200,
            payload=p,
            headers={"Cache-Control": "max-age=60"},
        )

        assert api.find_clan_by_tag("ABC") == dict(tag="#ABC")
