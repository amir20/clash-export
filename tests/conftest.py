import json
import os

import pytest

from clashleaders import app
from clashleaders.model import *

parent = os.path.abspath(os.path.dirname(__file__))


def object_from_json(file, obj):
    with open(os.path.join(parent, "fixtures/" + file)) as f:
        return obj.from_json(f.read())


def historical_players_from_json(file):
    with open(os.path.join(parent, "fixtures/" + file)) as f:
        array = json.load(f)
        return [HistoricalPlayer.from_json(json.dumps(s)) for s in array]


@pytest.fixture
def clan(mocker, historical_clan_now, historical_clan_before):
    clan = object_from_json("clan.json", Clan)
    clan.historical_near_now = lambda: historical_clan_now
    clan.historical_near_now = lambda: historical_clan_now

    mocker.patch(
        "clashleaders.model.HistoricalClan.find_by_tag_near_time",
        return_value=historical_clan_before,
    )

    return clan


@pytest.fixture
def historical_clan_now():
    historical = object_from_json("historical_clan_now.json", HistoricalClan)
    historical.players = historical_players_from_json("players_now.json")

    return historical


@pytest.fixture
def historical_clan_before():
    historical = object_from_json("historical_clan_before.json", HistoricalClan)
    historical.players = historical_players_from_json("players_before.json")

    return historical


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
