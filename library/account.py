import logging
import jwt
import os
from passlib.hash import pbkdf2_sha512

from odm.account import Account as OdmAccount


class Account:
    def __init__(self):
        pass

    def verify(self, email: str, password: str) -> (bool, dict):
        logging.info('account verify - prepare account verify check')

        account = OdmAccount.objects(email=email).only(
            'password',
            'token',
            'providers'
        ).first()

        if account:
            logging.info('account found, check login data')

            if pbkdf2_sha512.verify(password, account['password']):
                logging.info('login success')

                token_encode = jwt.encode({
                    'id': str(account.pk),
                    'token': account.token
                }, os.getenv('JWT_TOKEN_SECRET'), algorithm='HS256')

                return True, {
                    'token': token_encode.decode('ascii'),
                    'providers': account.providers,
                    'id': str(account.pk),
                }
            else:
                logging.info('login failure')
                return False, {}
        else:
            logging.info('account not found')
            return False, {}
