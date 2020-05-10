import logging
import jwt
import os
import uuid
from urllib.parse import urlencode
from passlib.hash import pbkdf2_sha512
from email_validator import validate_email, EmailNotValidError
from mongoengine import DoesNotExist

from odm.account import Account as OdmAccount
from odm.accessToken import AccessToken as OdmAccessToken


class Account:
    def __init__(self, account_id: str = None):
        if account_id is not None:
            pass

        else:
            self.__account = OdmAccount()

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

    @staticmethod
    def __confirm_strong_password(password: str) -> bool:
        l, u, d, p = 0, 0, 0, 0
        char_list = [char for char in '!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~']

        if len(password) >= 8:
            for i in password:
                if i.islower():
                    l += 1
                elif i.isupper():
                    u += 1
                elif i.isdigit():
                    d += 1
                elif i in char_list:
                    p += 1

        if l > 0 and u > 0 and p > 0 and d > 0 and (l+p+u+d) == len(password):
            return True
        else:
            return False

    def validate(self, data: dict, action: str = 'create') -> (bool, list):
        resp = True
        msg = []

        if action == 'create':
            if not data.get('first_name') or data.get('first_name') == '':
                resp = False
                msg.append('Your need a first name')

            if not data.get('last_name') or data.get('last_name') == '':
                resp = False
                msg.append('Your need a last name')

            if not data.get('email') or data.get('email') == '':
                resp = False
                msg.append('Your need a email')
            else:
                try:
                    validate_email(data.get('email'))

                    try:
                        OdmAccount.objects.get(email=data.get('email'))
                        resp = False
                        msg.append('Account with this e-mail allready exists.')
                    except DoesNotExist:
                        pass


                except EmailNotValidError as e:
                    resp = False
                    msg.append('E-mail not validated')

            if not data.get('password') or not data.get('password_confirm') or data.get('password') == '':
                resp = False
                msg.append('Password can be empty')
            elif data.get('password') != data.get('password_confirm'):
                resp = False
                msg.append('The 2 passwords its not equal.')
            elif not self.__confirm_strong_password(password=data.get('password')):
                resp = False
                msg.append('Your password its to weak.')

        return resp, msg

    def create(self, data: dict, sign_in: bool = False, access_token: str = None, url_args: dict = {}) -> (bool, list, str, int):
        resp, msg = self.validate(data=data)
        url_redirect = ''
        status_code = 0

        if resp:
            try:
                self.__account.email = data.get('email')
                self.__account.password = pbkdf2_sha512.hash(data.get('password'))
                self.__account.token = str(uuid.uuid4())
                self.__account.first_name = data.get('first_name')
                self.__account.last_name = data.get('last_name')
                self.__account.save()

                # Sending e-mail out if success created!

                if sign_in:
                    account_verify, account_data = self.verify(email=data.get('email'), password=data.get('password'))

                    if not account_verify:
                        url_redirect = f'/form/sign-in?{urlencode(url_args)}'
                        status_code = 302

                    else:
                        access_token = OdmAccessToken.objects(access_token=access_token)
                        access_token.update(**{
                            'set__account_id': account_data['id'],
                            'set__account_token': account_data['token']
                        })

                        url_redirect = f'/form/confirm-access?{urlencode(url_args)}'
                        status_code = 302

            except Exception as e:
                print(e)

        return resp, msg, url_redirect, status_code
