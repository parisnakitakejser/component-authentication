import os
import logging
from werkzeug.wrappers import Request, Response
from mongoengine import connect

from library.auth import AuthToken
from odm.account import Account

class AuthTokenCheck:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        environ['auth_token'] = None
        environ['auth_success'] = None
        environ['session_id'] = None

        auth_token = request.headers['X-AUTH-TOKEN'] if 'X-AUTH-TOKEN' in request.headers else None
        if auth_token is not None:
            logging.info('middleware: token found in headers, try to verify it')

            token_verify = AuthToken.verify(token=auth_token)

            if token_verify:
                logging.info('middleware: token verify success')
                environ['auth_token'] = AuthToken.decode_token(auth_token)
                environ['auth_success'] = True
                environ['session_id'] = request.headers['X-SESSION-ID'] if 'X-SESSION-ID' in request.headers else None

                account = Account.objects.get(pk=environ['auth_token']['id'])
                environ['administrator'] = account.administrator
                environ['providers'] = account.providers

            else:
                logging.info('middleware: token verify failed')
                environ['auth_success'] = False
        else:
            logging.info('middleware: token not found in headers')

        return self.app(environ, start_response)


class DBConnect:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            connect(
                db=os.getenv('MONGO_DATABASE') if os.getenv('MONGO_DATABASE') else 'component-authentication',
                host=os.getenv('MONGO_HOST'),
                port=int(os.getenv('MONGO_PORT')) if os.getenv('MONGO_PORT') else None,
                username=os.getenv('MONGO_USERNAME'),
                password=os.getenv('MONGO_PASSWORD'),
                authentication_source=os.getenv('MONGO_AUTH_SOURCE'),
                authentication_mechanism=os.getenv('MONGO_MECHANISM')
            )
            logging.info('Connection to mongo success')
            return self.app(environ, start_response)

        except Exception as e:
            logging.info('Connection to mongo failed')
            logging.info('Connection error:', e)

            res = Response(u'Connection to mongo failed', mimetype='text/plain', status=501)
            return res(environ, start_response)



