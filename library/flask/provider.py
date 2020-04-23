import logging
from flask import Response, request
from bson.json_util import dumps

from library.provider import Provider


class FlaskProvider:
    @staticmethod
    def create():
        logging.info('create provider')

        json_data = request.get_json()

        if request.environ['auth_success']:
            if request.environ['administrator']:
                provider = Provider()

                return Response(dumps({
                    'status': 'OK',
                    'content': provider.create(
                        name=json_data['name'],
                        allow_guest_signup=json_data['allow_guest_signup'],
                    )
                }), mimetype='text/json'), 200

            else:
                logging.info('create provider - account is not a administrator')

                return Response(dumps({
                    'status': 'Forbidden'
                }), mimetype='text/json'), 403

        else:
            logging.info('create provider - auth token not success')

            return Response(dumps({
                'status': 'Unauthorized'
            }), mimetype='text/json'), 401
