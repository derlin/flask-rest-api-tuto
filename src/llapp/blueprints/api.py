import wtforms
from flask import Blueprint, jsonify, request
from flask_wtf import FlaskForm

bp_api = Blueprint('api', __name__)


class Form(FlaskForm):

    def __init__(self, *args, **kwargs):
        kwargs['meta'] = kwargs.get('meta') or {}
        kwargs['meta'].setdefault('csrf', False)
        super().__init__(*args, **kwargs)

    def as_dict(self):
        return {k: self._fields[k].data for k, _ in self._unbound_fields}


class HelloParams(Form):
    name = wtforms.StringField(
        default='world', validators=[wtforms.validators.Length(max=50)])
    repeat = wtforms.IntegerField(
        default=1, render_kw={'type': 'number'},
        validators=[wtforms.validators.NumberRange(min=1, max=1000)])
    capitalize = wtforms.BooleanField(default=False)


@bp_api.route('/', methods=['GET', 'POST'])
def hello_world():
    # parse arguments
    params = HelloParams(request.args) if len(request.data) == 0 else HelloParams()
    # validate parameters
    if not params.validate():
        return jsonify(dict(message=params.errors)), 400
    # construct response
    hello = f'Hello {params.name.data.capitalize()} ' if params.capitalize.data else f'hello {params.name.data} '
    response = (hello * params.repeat.data).strip()
    return jsonify(dict(args=params.as_dict(), response=response))


@bp_api.route('/<int:id>/<string:name>', methods=['GET'])
def echo_params(id, name):
    args = request.args
    value = args.get('key', 'default')
    return jsonify(dict(id=id, name=name, value=value))
