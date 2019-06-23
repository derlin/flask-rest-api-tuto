from . import *

#
# for ids option in parametrize, see https://hackebrot.github.io/pytest-tricks/param_id_func/
#

@pytest.mark.parametrize('api', APIS)
@pytest.mark.parametrize(
    "params,expected",
    [
        (None, 'hello world'),
        (dict(name="lala"), 'hello lala'),
        (dict(name="lala", repeat=2), 'hello lala hello lala'),
        (dict(capitalize=True), 'Hello World'),
        (dict(name='lucy', repeat=3, capitalize=True), 'Hello Lucy Hello Lucy Hello Lucy')
    ],
    ids=['no args', 'name', 'name and repeat', 'capitalize', 'name repeat capitalize']
)
def test_get_api(client, api, params, expected):
    query_params = dict_to_query_params(params)
    response = client.get(f'/{api}?{query_params}')
    assert response.status_code in RESPONSE_OK

    json_res = parse_json_response(response)
    assert expected == json_res['response']


@pytest.mark.parametrize('api', APIS)
@pytest.mark.parametrize(
    "params,body,expected",
    [
        (None, None, 'hello world'),
        (dict(name="lala"), None, 'hello lala'),
        (None, dict(name="lala", repeat=2), 'hello lala hello lala')
    ],
    ids=['no argument', 'query param (name)', 'body param (name,repeat)']
)
def test_post_api(client, api, params, body, expected):
    query_params = dict_to_query_params(params)
    endpoint = f'/{api}?{query_params}'
    response = client.post(endpoint) if body is None else client.post(endpoint, json=body)
    assert response.status_code in RESPONSE_OK

    json_res = parse_json_response(response)
    assert expected == json_res['response']


@pytest.mark.parametrize('api', APIS)
@pytest.mark.parametrize('method', ['GET', 'POST'])
@pytest.mark.parametrize(
    "params",
    [
        (dict(repeat=-1)),
        (dict(repeat=100000))
    ],
    ids=['repeat negative', 'repeat too big']
)
def test_errors(client, api, method, params):
    if method == 'GET':
        query_params = dict_to_query_params(params)
        response = client.get(f'/{api}?{query_params}')
    else:
        response = client.post(f'/{api}', json=params)
    assert response.status_code == 400

    json_res = json.loads(response.data)
    assert 'message' in json_res
    for key in params.keys():
        assert key in json_res['message']
