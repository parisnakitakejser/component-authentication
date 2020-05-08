from typing import Union
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import string
import logging
from mongoengine import DoesNotExist

from library.auth import AuthToken

from odm.accessToken import AccessToken as OdmAccessToken
from odm.provider import Provider as OdmProvider


class AccessToken:
    def __init__(self, token: Union[str, None] = None) -> None:
        if token is not None:
            try:
                self.__access_token = OdmAccessToken.objects.get(access_token=token)
            except DoesNotExist:
                raise DoesNotExist()
        else:
            self.__access_token = OdmAccessToken()

    def generate(self, provider_id: str) -> str:
        self.__access_token.access_token = ''.join(random.choices(string.ascii_letters + string.digits, k=128))
        self.__access_token.provider_id = provider_id
        self.__access_token.expired_at = datetime.utcnow() + timedelta(minutes=30)
        self.__access_token.created_at = datetime.utcnow()
        self.__access_token.save()

        return self.__access_token.access_token

    def verify(self) -> (bool, Union[ObjectId, None]):
        if self.__access_token.expired_at >= datetime.utcnow():
            self.__access_token.update(**{
                'expired_at': datetime.utcnow() + timedelta(minutes=30),
                'updated_at': datetime.utcnow()
            })

            return True, self.__access_token.provider_id

        else:
            return False, None

    def verify_access_token(self, provider_id: str, provider_secret: str) -> (bool, dict):
        if self.__access_token.provider_id == ObjectId(provider_id):
            verify, _ = self.verify()

            if not verify:
                logging.info('access token expired')
                return False, {}

            try:
                OdmProvider.objects.get(pk=provider_id, secret_key_private=provider_secret)
                logging.info('provider_id and secret_key allowed to get access for this provider')
            except DoesNotExist:
                logging.info('provider_id and secret_key do not match')
                return False, {}

            if AuthToken.verify(token=self.__access_token.account_token):
                token = AuthToken.decode_token(token=self.__access_token.account_token)

                if 'token' in token:
                    del token['token']
                    
                return True, {
                    'jwt': self.__access_token.access_token,
                    'data': token
                }
            else:
                logging.info('account token is not verify')
                return False, {}
        else:
            logging.info('provider_id not match access_token provider_id')
            return False, {}
