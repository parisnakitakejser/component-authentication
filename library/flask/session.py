from flask import Response, request
from bson.json_util import dumps


class FlaskSession:
    @staticmethod
    def get():
        print(request.environ['auth_token'])
        print(request.environ['auth_success'])
        print(request.environ['session_id'])

        return Response(dumps({
            'status': 'OK',
        }), mimetype='text/json'), 200

    @staticmethod
    def update():
        pass