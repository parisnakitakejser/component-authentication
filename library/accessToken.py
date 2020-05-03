from typing import Union
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import random
import string
from mongoengine import DoesNotExist

from odm.accessToken import AccessToken as OdmAccessToken


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
