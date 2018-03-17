import clashleaders.views.clan


def test_detail_page_oldest_days(client, mocker, clan_pre_calculated):
    patch_all(mocker, clan_pre_calculated)
    client.get('/clan/reddit-dynasty-ugjpvjr')

    clashleaders.views.clan.render_template.assert_called_once_with('clan.html',
                                                                    clan=clan_pre_calculated,
                                                                    oldest_days=12,
                                                                    players=mocker.ANY,
                                                                    similar_clans=mocker.ANY,
                                                                    description=mocker.ANY,
                                                                    similar_clans_start_count=mocker.ANY)


def test_detail_page_status(client, mocker, clan_pre_calculated):
    patch_all(mocker, clan_pre_calculated)
    r = client.get('/clan/reddit-dynasty-ugjpvjr')
    assert r.status_code == 500  # Should fix this later


def patch_all(mocker, clan_pre_calculated):
    mocker.patch('clashleaders.model.ClanPreCalculated.find_by_slug', return_value=clan_pre_calculated)
    mocker.patch('clashleaders.views.clan.update_page_views')
    mocker.patch('clashleaders.views.clan.render_template')
