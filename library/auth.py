import os
import jwt
import logging
from mongoengine.errors import DoesNotExist

from odm.account import Account


class AuthToken:
    @staticmethod
    def decode_token(token: str):
        try:
            token = jwt.decode(token, os.getenv('JWT_TOKEN_SECRET'), algorithms=['HS256'])
            logging.info('Decode token is success')
        except jwt.DecodeError:
            token = None
            logging.info('Decode token is failed')

        return token

    @staticmethod
    def verify(token: str):
        logging.info('Token verify lookup')
        token = AuthToken.decode_token(token=token)

        if token:
            try:
                account = Account.objects.get(pk=token['id'], token=token['token'])
                logging.info('Account match the query, token verify success')
                return True
            except DoesNotExist:
                logging.info('Account not match the query, token failed')
                return False
        else:
            return None



        return token
