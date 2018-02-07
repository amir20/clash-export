import pytest
import os

from clashleaders.model import Clan, ClanPreCalculated
from clashleaders import app

parent = os.path.abspath(os.path.dirname(__file__))


def object_from_json(file, obj):
    with open(os.path.join(parent, "fixtures/" + file)) as f:
        return obj.from_json(f.read())


@pytest.fixture
def clan_with_players():
    return object_from_json("clan_with_players.json", Clan)


@pytest.fixture
def clan_season_start():
    return object_from_json("clan_season_start.json", Clan)


@pytest.fixture
def first_clan_with_players():
    return object_from_json("first_clan_with_players.json", Clan)


@pytest.fixture
def clan_pre_calculated():
    cpc = object_from_json("clan_pre_calculated.json", ClanPreCalculated)
    cpc.season_start = clan_season_start()
    cpc.most_recent = clan_with_players()

    return cpc


@pytest.fixture
def clan_table_html():
    with open(os.path.join(parent, "fixtures/clan-table.html")) as f:
        return f.read()


@pytest.fixture
def client():
    return app.test_client()
