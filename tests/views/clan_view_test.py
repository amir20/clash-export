from collections import defaultdict

from clashleaders.model import Status


def test_detail(client, mocker, clan):
    patch_all(mocker, clan)
    r = client.get("/clan/reddit-dynasty-ugjpvjr")

    assert b'<body class="clan_detail_page">' in r.data


def test_detail_page_status(client, mocker, clan):
    patch_all(mocker, clan)
    r = client.get("/clan/reddit-dynasty-ugjpvjr")
    assert r.status_code == 200


def patch_all(mocker, clan):
    mocker.patch("clashleaders.model.Clan.find_by_slug", return_value=clan)
    mocker.patch("clashleaders.model.Status.instance", return_value=Status())
    mocker.patch("clashleaders.views.static.fetch_changelog", return_value=[])
    mocker.patch("clashleaders.views.manifest_map", return_value=defaultdict(lambda: "../tests/fixtures/dummy.txt"))
    mocker.patch.object(clan, "similar_clans")
    mocker.patch.object(clan, "trophy_history")
    clan.similar_clans.return_value = [10, [clan]]
    clan.trophy_history.return_value = []

    mocker.patch.object(clan, "days_of_history")
    clan.days_of_history.return_value = 7
