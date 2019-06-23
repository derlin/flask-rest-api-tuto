# pip install pytest
import json

import pytest
from llapp.__main__ import create_app

RESPONSE_OK = [302, 200]
APIS = ['api', 'flrapi']


@pytest.fixture(scope='module')
def client():
    app = create_app()
    # the following is not strictly necessary, but recommended
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['DEBUG'] = False

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    yield app.test_client()


def parse_json_response(response):
    json_res = json.loads(response.data)
    assert 'args' in json_res
    assert 'response' in json_res
    return json_res


def dict_to_query_params(d):
    if d is None:
        return ''
    return '&'.join(f'{k}={v}' for k, v in d.items())
