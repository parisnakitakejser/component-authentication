import logging
from bson.json_util import dumps
from flask import Response, request

from library.auth import AuthToken


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