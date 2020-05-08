import logging
from bson.json_util import dumps
from flask import Response, request

from library.auth import AuthToken
from library.accessToken import AccessToken


class FlaskToken:
    @staticmethod
    def verify():
        auth_token = request.headers['X-AUTH-TOKEN'] if 'X-AUTH-TOKEN' in request.headers else None

        if auth_token:
            token_verify = AuthToken.verify(token=auth_token)

            if token_verify:
                logging.info('Token verify - success - response 200')

                return Response(dumps({
                    'status': 'OK',
                    'verify': token_verify
                }), mimetype='text/json'), 200
            else:
                logging.info('Token verify - failed - response 401')

                return Response(dumps({
                    'status': 'Unauthorized',
                }), mimetype='text/json'), 401
        else:
            logging.info('Token verify - not exists - response 401')

            return Response(dumps({
                'status': 'Unauthorized',
            }), mimetype='text/json'), 401

    @staticmethod
    def verify_access_token():
        access_token = request.headers.get('X-ACCESS-TOKEN')
        provider_secret = request.headers.get('X-PROVIDER-SECRET')
        provider_id = request.headers.get('X-PROVIDER-ID')

        access_token = AccessToken(token=access_token)
        access_verify, token_data = access_token.verify_access_token(provider_id=provider_id, provider_secret=provider_secret)

        if access_verify:
            return Response(dumps({
                'status': 'OK',
                'token': {
                    'data': token_data['data'],
                    'jwt': token_data['jwt'],
                }
            }), mimetype='text/json'), 200
        else:
            return Response(dumps({
                'status': 'Unauthorized'
            }), mimetype='text/json'), 401
