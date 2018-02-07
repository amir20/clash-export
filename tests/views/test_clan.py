
def test_detail_page(client, mocker, clan_pre_calculated, first_clan_with_players, clan_table_html):
    mocker.patch('clashleaders.model.ClanPreCalculated.find_by_slug', return_value=clan_pre_calculated)
    mocker.patch('clashleaders.model.Clan.find_last_by_tag', return_value=first_clan_with_players)
    mocker.patch('clashleaders.views.clan.update_page_views')
    r = client.get('/clan/reddit-dynasty-ugjpvjr')
    assert r.status_code == 200

    assert clan_table_html.encode() in r.data
