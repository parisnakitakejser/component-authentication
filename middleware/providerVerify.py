from werkzeug.wrappers import Request, Response
from bson.objectid import ObjectId
from mongoengine import DoesNotExist
from urllib.parse import urlencode
import logging

from library.accessToken import AccessToken
from odm.provider import Provider as OdmProvider


class ProviderVerify:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        request = Request(environ)
        logging.info('middleware: Provider Verify')

        request_method = request.environ['REQUEST_METHOD']
        request_path = request.environ['PATH_INFO']
        request_verify = f'{request_path}#{request_method}'

        provider_id = request.headers['X-PROVIDER-ID'] if 'X-PROVIDER-ID' in request.headers else request.args.get('id')
        provider_secret = request.headers['X-PROVIDER-SECRET'] if 'X-PROVIDER-SECRET' in request.headers else None

        environ['provider'] = None

        none_provider_check = (
            '/static/',
            '/favicon.ico'
        )

        provider_public_check = (
            '/form/'
        )

        if request_path.lower().startswith(none_provider_check):
            logging.info(f'middleware: {request_path.lower()} - do not provider check this path')

        elif request_path.lower().startswith(provider_public_check):
            logging.info(f'middleware: {request_path.lower()} - do public secret or access token check for this path')

            access_token = request.args.get('access_token')
            provider_public = request.args.get('token')

            if access_token is not None:
                try:
                    access_token = AccessToken(token=access_token)
                    verify_response, provider_id = access_token.verify()

                    if not verify_response:
                        logging.info('Token is expired')

                        res = Response(u'Gone', mimetype='text/plain', status=410)
                        return res(environ, start_response)

                    else:
                        environ['provider'] = {
                            'id': provider_id
                        }

                except DoesNotExist:
                    logging.info('Token not found or expired')
                    res = Response(u'Gone', mimetype='text/plain', status=410)
                    return res(environ, start_response)


            else:
                logging.info('middleware: provider check prepare')

                try:
                    provider = OdmProvider.objects.get(pk=provider_id, secret_key_public=provider_public)
                    logging.info('middleware: provider check - exists and ready')

                    access_token = AccessToken()
                    token = access_token.generate(provider_id=provider_id)

                    url_args = dict(request.args)
                    del url_args['id']
                    del url_args['token']
                    url_args['access_token'] = token

                    status = '302 Found'
                    headers = [
                        ('Location', f'{request_path}?{urlencode(url_args)}'),
                        ('Content-Length', '0')
                    ]

                    start_response(status, headers)
                    return ['']

                except DoesNotExist:
                    logging.info('middleware: provider not found based on provider_id and public key')
                    res = Response(u'Forbidden', mimetype='text/plain', status=403)
                    return res(environ, start_response)
        else:
            if request_verify not in ['/account/sign-in#GET', '/account#PUT']:
                if not request.environ['administrator'] and provider_id is None:
                  logging.info('middleware: provider_id not found in header or query params')

                  res = Response(u'X-PROVIDER-ID not found in headers or id in query params', mimetype='text/plain', status=501)

                  return res(environ, start_response)

                elif request.environ['administrator']:
                    logging.info('middleware: Account is administrator')
                    if provider_id is not None:
                        try:
                            provider = OdmProvider.objects.get(pk=provider_id)
                            environ['provider'] = {
                                'name': provider.name,
                                'id': provider_id
                            }
                        except DoesNotExist:
                            logging.info('middleware: administrator - provider not found in database.')
                            res = Response(u'Provider not found with this provider_id', mimetype='text/plain', status=403)

                            return res(environ, start_response)

                else:
                    logging.info('middleware: Account is normal')

                    if ObjectId(provider_id) in request.environ['providers']:
                        logging.info('middleware: Account match provider_id and allowed to access')

                        try:
                            provider = OdmProvider.objects.get(pk=provider_id, secret_key_private=provider_secret)
                            environ['provider'] = {
                                'name': provider.name,
                                'id': provider_id
                            }
                        except DoesNotExist:
                            logging.info('middleware: provider secret or provider_id did not match in the database.')
                            res = Response(u'Account did not have access for this provider', mimetype='text/plain', status=403)

                            return res(environ, start_response)

                    else:
                        logging.info('middleware: Account do not match eny provider_id, and do not have access')
                        res = Response(u'Account did not have access for this provider', mimetype='text/plain', status=403)

                        return res(environ, start_response)
            else:
                logging.info('middleware: Account try to sign in or create a new account')

        return self.app(environ, start_response)