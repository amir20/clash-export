import pytest
import os


from clashleaders.model import Clan

parent = os.path.abspath(os.path.dirname(__file__))


def clan_from_json(file):
    with open(os.path.join(parent, "fixtures/" + file)) as f:
        return Clan.from_json(f.read())


@pytest.fixture
def clan_with_players():
    return clan_from_json("clan_with_players.json")
