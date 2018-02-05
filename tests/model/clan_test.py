import pytest

from clashleaders.model import Clan
from datetime import datetime
from bson.objectid import ObjectId


def test_find_last_by_tag_with_hash(mocker):
    mocker.patch('clashleaders.model.Clan.objects')
    Clan.find_last_by_tag('#XYZ')
    Clan.objects.assert_called_once_with(tag='#XYZ')


def test_find_last_by_tag_without_hash(mocker):
    mocker.patch('clashleaders.model.Clan.objects')
    Clan.find_last_by_tag('XYZ')
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


@pytest.mark.freeze_time('2018-05-20 12:00:01')
def tst_find_first_by_tag(mocker):
    mocker.patch('clashleaders.model.Clan.from_now_with_tag')
    Clan.from_now_with_tag('EFGH')
    Clan.from_now_with_tag.assert_called_once_with(tag='#EFGH', hours=13)
