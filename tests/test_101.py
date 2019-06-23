# pip install pytest

from . import *


@pytest.mark.parametrize("endpoint", ['/', '/specification', '/showcase', '/api', '/flrapi'])
def test_get(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code in RESPONSE_OK


@pytest.mark.parametrize(
    "path,code",
    [('/not@@exist', 404),
     ('/api?name=' + ('long' * 50), 400)],
    ids=['not found', 'api name too long']
)
def test_exceptions(client, path, code):
    response = client.get(path)
    assert response.status_code == code
    assert 'json' in response.content_type
    json_res = json.loads(response.data)
    assert 'message' in json_res
