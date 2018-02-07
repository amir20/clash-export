
def test_detail_page(client, mocker, clan_pre_calculated):
    mocker.patch('clashleaders.model.ClanPreCalculated.find_by_slug', return_value=clan_pre_calculated)

    r = client.get('/clan/reddit-dynasty-ugjpvjr')
    assert r.status_code == 200
