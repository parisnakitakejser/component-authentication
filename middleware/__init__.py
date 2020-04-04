import os
import logging
from werkzeug.wrappers import Request, Response
from mongoengine import connect


class AuthTokenCheck:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        logging.info('AuthToken check - OK')

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



