from mkad_distance import create_app

def test_shorten(client):
    response = client.get('/')
    assert b"Moscow Ring Road Distance Calculator" in response.data

def test_shorten(client):
    response = client.get('/clear_key')
    assert b"Clear Yandex API-Key" not in response.data

def test_shorten(client):
    response = client.get('/clear_log')
    assert b"address_log" not in client.session.keys()

def test_shorten(client):
    response = client.get('/log')
    assert b"Log Distances" in response.data

def test_shorten(client):
    response = client.get('/get_distance')
    assert b"Address coordinates are" or "Total distance from" in response.data

