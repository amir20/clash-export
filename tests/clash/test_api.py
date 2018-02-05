import pytest

from clashleaders.clash import api


def test_find_clan_bad(mocker):
    r = mocker.Mock()
    r.status_code = 400
    mocker.patch('requests.get', return_value=r)
    with pytest.raises(api.ClanNotFound):
        api.find_clan_by_tag('ABC')


def test_find_clan_success(mocker):
    r = mocker.Mock()
    r.json = mocker.Mock()
    r.status_code = 200

    mocker.patch('requests.get', return_value=r)
    api.find_clan_by_tag('ABC')

    r.json.assert_called_once_with()
