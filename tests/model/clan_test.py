from clashleaders.model import Clan


def test_find_by_tag(mocker):
    mocker.patch("clashleaders.model.Clan.objects")
    Clan.find_by_tag("xyz")
    Clan.objects.assert_called_once_with(tag="#XYZ")
