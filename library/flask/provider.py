import logging
from flask import Response, request
from bson.json_util import dumps
from bson.objectid import ObjectId
from mongoengine import DoesNotExist

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

    @staticmethod
    def get():
        logging.info('get provider')

        if request.environ['auth_success']:
            provider_id = request.args.get('id')

            try:
                provider = Provider(provider_id=provider_id)
            except DoesNotExist:
                return Response(dumps({
                    'status': 'Not Found'
                }), mimetype='text/json'), 404

            if request.environ['administrator'] or ObjectId(request.environ['auth_token']['id']) in provider.administrators:
                logging.info(f'provider found with id: {provider_id}, account allowed to return data')

                return Response(dumps({
                    'status': 'OK',
                    'content': provider.get_content()
                }), mimetype='text/json'), 200
            else:
                logging.info(f'provider found with id: {provider_id}, but account its not allowed to return data')

                return Response(dumps({
                    'status': 'Forbidden',
                }), mimetype='text/json'), 403

        else:
            logging.info('get provider - auth token is not success')
            return Response(dumps({
                'status': 'Unauthorized'
            }), mimetype='text/json'), 401

    @staticmethod
    def update():
        pass
