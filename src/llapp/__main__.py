#!/usr/bin/env python3
from urllib.error import HTTPError

from flask import Flask, make_response, jsonify

# WARNING: ensure you use full imports here
from llapp.blueprints.showcase import bp_showcase
from llapp.blueprints.api import bp_api

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = '8080'

# --- APP AND BLUEPRINT

app = Flask(__name__)

# required for forms (if wtforms is used)
# app.config.update(dict(
#     SECRET_KEY="powerful secretkey",
#     WTF_CSRF_SECRET_KEY="a csrf secret key"
# ))


app.register_blueprint(bp_showcase, url_prefix='/showcase')
app.register_blueprint(bp_api, url_prefix='/api')


# --- ERROR HANDLING (json)

@app.errorhandler(Exception)
def any(error):
    error_code = 400 if isinstance(error, HTTPError) else 500
    return make_response(jsonify(error=str(error)), error_code)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(error='Not found'), 404)


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


# --- LAUNCH COMMAND & MAIN

def setup_app(debug=False, **kwargs):
    if debug: app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['TRAP_HTTP_EXCEPTIONS'] = True
    # use strict_slashes false so that when a blueprint with an index route ('/') is registered with an URL prefix,
    # such as 'showcase', get /showcase will work as well (will redirect to /showcase/)
    app.url_map.strict_slashes = False
    return app


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', help='run in debug mode', action='store_true')
    parser.add_argument('--threaded', help='activate threading', action='store_true')
    parser.add_argument('--host', default=DEFAULT_HOST, type=str)
    parser.add_argument('--port', default=DEFAULT_PORT, type=str)
    args = vars(parser.parse_args())

    setup_app(**args).run(**args)
