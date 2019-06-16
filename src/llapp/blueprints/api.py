from flask import Blueprint, jsonify

bp_api = Blueprint('api', __name__)


@bp_api.route('/', methods=['GET'])
def hello_world():
    return jsonify(dict(message='hello world'))
