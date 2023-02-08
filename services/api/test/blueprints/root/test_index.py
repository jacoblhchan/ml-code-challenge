def test_root_index(client):
    # GET /
    response = client.get('/')

    # Should successfully return
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data == 'Hello, from Flask!'


def test_non_existent_route(client):
    # GET /dne
    response = client.get('/dne')

    # Should return a 404
    assert response.status_code == 404

