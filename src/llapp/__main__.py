#!/usr/bin/env python3

from urllib.error import HTTPError

import click
from flask import Flask, make_response, jsonify
from flask.cli import FlaskGroup

# WARNING: ensure you use full imports here
from llapp.blueprints.api import bp_api
from llapp.blueprints.flrapi import bp_flrapi
from llapp.blueprints.showcase import bp_showcase


# --- CREATING THE APP

def create_app(k=None):
    print(f'arguments: k={k}')

    app = Flask(__name__)

    if app.config['DEBUG']: app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    # use strict_slashes false so that when a blueprint with an index route ('/') is registered with an URL prefix,
    # such as 'showcase', get /showcase will work as well (will redirect to /showcase/)
    app.url_map.strict_slashes = False

    # required for forms (if wtforms is used)
    app.config.update(dict(
        SECRET_KEY="powerful secretkey",
        WTF_CSRF_SECRET_KEY="a csrf secret key"
    ))

    app.register_blueprint(bp_showcase, url_prefix='/showcase')
    app.register_blueprint(bp_api, url_prefix='/api')
    app.register_blueprint(bp_flrapi, url_prefix='/flrapi')

    # --- ERROR HANDLING (json)

    @app.errorhandler(Exception)
    def any(error):
        error_code = 400 if isinstance(error, HTTPError) else 500
        return make_response(jsonify(message=str(error)), error_code)

    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify(message='Not found'), 404)

    # --- JINJA (used in template wtf.html, only used in showcase)

    def is_hidden_field(field):
        from wtforms import HiddenField
        return isinstance(field, HiddenField)

    app.jinja_env.globals['bootstrap_is_hidden_field'] = is_hidden_field

    # --- LITTLE ROUTES

    @app.route('/specification')
    def serve_specs():
        # to make it downloadable, use:
        # from flask import redirect, url_for
        # redirect(url_for('static'), filename='/spec.yaml')

        # but I want the file to be displayed in the browser (not as attachment)
        # so I use this:
        from flask import current_app, Response
        with current_app.open_resource('static/spec.yaml') as f:
            return Response(f.read(), mimetype='text/yaml')

    @app.route('/')
    def redirecto_showcase():
        from flask import redirect, url_for
        return redirect(url_for('showcase.index'))

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
@click.option('-k', default=None)
def cli(**kwargs):
    return create_app(**kwargs)


if __name__ == "__main__":
    cli()
