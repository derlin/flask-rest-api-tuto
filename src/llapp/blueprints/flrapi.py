from flask import Blueprint, request
from flask_restful import Resource, reqparse, Api

bp_flrapi = Blueprint('flask-restful-api', __name__)


def _add_argument(parser, name, **kwargs):
    # by default, any query with Content-Type: application/json and an
    # empty body will throw an error. To circumvent that, ask reqparse to
    # look only in the query params if the body is empty.
    if not 'location' in kwargs and len(request.data) == 0:
        kwargs['location'] = 'args'
    parser.add_argument(name, **kwargs)


def int_range(min=None, max=None):
    def validate(s):
        try:
            i = int(s)
        except:
            raise ValueError(f'{s} must be an int.')
        if min is not None and i < min:
            raise ValueError(f'Int must be < {min}')
        if max is not None and i > max:
            raise ValueError(f'Int must be > {max}')
        return i

    return validate


class HelloResource(Resource):

    def get(self):
        return self._handle()

    def post(self):
        return self._handle()

    def _handle(self):
        parser = reqparse.RequestParser()
        _add_argument(parser, 'name', type=str, default='world')
        _add_argument(parser, 'repeat', type=int_range(min=1, max=1000), default=1)
        _add_argument(parser, 'capitalize', type=bool, default=False)

        args = parser.parse_args()

        hello = f"Hello {args['name'].capitalize()} " if args['capitalize'] else f"hello {args['name']} "
        response = (hello * args['repeat']).strip()
        return dict(args=args, response=response)


rest_api = Api(bp_flrapi)
rest_api.add_resource(HelloResource, '/', endpoint='index')
