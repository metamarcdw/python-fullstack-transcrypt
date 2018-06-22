from flask import url_for

def test_get_all_users_unauthorized(client):
    res = client.get(url_for('users_resource'))
    assert res.status_code == 401
