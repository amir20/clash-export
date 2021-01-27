from collections import defaultdict

import clashleaders.views.clan
from clashleaders.model import Status


def test_detail_page_oldest_days(client, mocker, clan):
    patch_all(mocker, clan)
    client.get("/clan/reddit-dynasty-ugjpvjr")

    clashleaders.views.clan.render_template.assert_called_once_with(
        "clan.html",
        clan=clan,
        initial_state=mocker.ANY,
    )


def test_detail_page_status(client, mocker, clan):
    patch_all(mocker, clan)
    r = client.get("/clan/reddit-dynasty-ugjpvjr")
    assert r.status_code == 500  # Should fix this later


def patch_all(mocker, clan):
    mocker.patch("clashleaders.model.Clan.find_by_slug", return_value=clan)
    mocker.patch("clashleaders.model.Status.instance", return_value=Status())
    mocker.patch("clashleaders.views.static.fetch_changelog", return_value=[])
    mocker.patch("clashleaders.views.manifest_map", return_value=defaultdict(lambda: "../tests/fixtures/dummy.txt"))
    mocker.patch("clashleaders.views.clan.render_template")
    mocker.patch.object(clan, "similar_clans")
    mocker.patch.object(clan, "trophy_history")
    clan.similar_clans.return_value = [10, [clan]]
    clan.trophy_history.return_value = []

    mocker.patch.object(clan, "days_of_history")
    clan.days_of_history.return_value = 7
