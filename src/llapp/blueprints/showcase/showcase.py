import json

from flask import Blueprint, render_template, request, url_for
from wtforms import SubmitField

from ..api import hello_world, HelloParams

bp_showcase = Blueprint('showcase', __name__, template_folder='.')


class HelloForm(HelloParams):
    submit = SubmitField()

    def as_dict(self):
        d = super().as_dict()
        del d['submit']
        return d


@bp_showcase.route('/', methods=['GET'])
def index():
    form = HelloForm(request.args)
    return_args = dict(form=form)
    if form.validate():
        body = json.loads(hello_world().data)
        return_args['response'] = body['response']
        return_args['endpoint'] = url_for('api.hello_world', _external=True, **form.as_dict())
    return render_template('showcase.html', **return_args)
