from datetime import datetime

import pytest
from bson.objectid import ObjectId

from clashleaders.model import Clan


def test_find_last_by_tag_with_hash(mocker):
    mocker.patch('clashleaders.model.Clan.objects')
    Clan.find_least_recent_by_tag('#XYZ')
    Clan.objects.assert_called_once_with(tag='#XYZ')


def test_find_last_by_tag_without_hash(mocker):
    mocker.patch('clashleaders.model.Clan.objects')
    Clan.find_least_recent_by_tag('XYZ')
    Clan.objects.assert_called_once_with(tag='#XYZ')


@pytest.mark.freeze_time('2018-05-20 12:00:01')
def test_from_now(mocker):
    mocker.patch('clashleaders.model.Clan.objects')
    Clan.from_now(days=3)
    id = ObjectId.from_datetime(datetime(2018, 5, 17, 12, 0, 1))
    Clan.objects.assert_called_once_with(id__gte=id)


@pytest.mark.freeze_time('2018-05-20 12:00:01')
def test_older_than(mocker):
    mocker.patch('clashleaders.model.Clan.objects')
    Clan.older_than(days=3)
    id = ObjectId.from_datetime(datetime(2018, 5, 17, 12, 0, 1))
    Clan.objects.assert_called_once_with(id__lt=id)


@pytest.mark.freeze_time('2018-05-20 12:00:01')
def test_from_now_with_tag(mocker):
    mocker.patch('clashleaders.model.Clan.objects')
    Clan.from_now_with_tag('ABCD', days=8)
    id = ObjectId.from_datetime(datetime(2018, 5, 12, 12, 0, 1))
    Clan.objects.assert_called_once_with(id__gte=id, tag='#ABCD')


def test_clan_to_player_matrix(clan_with_players, snapshot):
    data = clan_with_players.to_player_matrix()
    snapshot.assert_match(data)
