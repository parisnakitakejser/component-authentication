import logging
from flask import Response, request
from bson.json_util import dumps

from library.session import Session


class FlaskSession:
    @staticmethod
    def get():
        logging.info('get session')

        if request.environ['auth_success']:
            account_id = request.environ['auth_token']['id']
            session_id = request.environ['session_id']

            logging.info(f'session allowed - select session data from account: {account_id}')

            session_id, session_data = Session.get(account_id=account_id, session_id=session_id)

            if session_id:
                logging.info(f'session found and return to client for account: {account_id} with session_id: {session_id}')

                return Response(dumps({
                    'status': 'OK',
                    'session_id': session_id,
                    'session_data': session_data
                }), mimetype='text/json'), 200

            else:
                logging.info(f'session not allowed - account_id: {account_id} trying to get session_id: {session_id} and its not the right owner.')
                return Response(dumps({
                    'status': 'Forbidden',
                }), mimetype='text/json'), 403
        else:
            logging.info('session not allowed - auth token not verify')

            return Response(dumps({
                'status': 'Unauthorized',
            }), mimetype='text/json'), 401

    @staticmethod
    def update():
        logging.info('update session')

        if request.environ['auth_success']:
            json_data = request.get_json()

            account_id = request.environ['auth_token']['id']
            session_id = request.environ['session_id']

            logging.info(f'session allowed - select session data from account: {account_id}')

            session_id, session_data = Session.update(account_id=account_id, session_id=session_id, session_data=json_data)
            if session_id is not None:
                logging.info(f'session allowed - account: {account_id} updated session: {session_id} with new data')

                return Response(dumps({
                    'status': 'OK',
                    'session_id': session_id,
                    'session_data': session_data
                }), mimetype='text/json'), 200

            else:
                logging.info(f'session not allowed - account_id: {account_id} trying to get session_id: {session_id} and its not the right owner.')
                return Response(dumps({
                    'status': 'Forbidden',
                }), mimetype='text/json'), 403

        else:
            logging.info('session not allowed - auth token not verify')

            return Response(dumps({
                'status': 'Unauthorized',
            }), mimetype='text/json'), 401