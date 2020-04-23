from typing import Union
import random
import string
import logging
from mongoengine import DoesNotExist

from odm.provider import Provider as OdmProvider


class Provider:
    administrators = []

    def __init__(self, provider_id: Union[str, None] = None):
        if provider_id is not None:
            try:
                self.__provider = OdmProvider.objects.get(pk=provider_id)
                self.administrators = self.__provider.administrators

                logging.info(f'provider_id: {provider_id} - found')
            except DoesNotExist:
                logging.info(f'provider_id: {provider_id} - not found')
                raise DoesNotExist
        else:
            self.__provider = OdmProvider()

    def create(self, name: str, allow_guest_signup: bool) -> dict:
        self.__provider.name = name
        self.__provider.allow_guest_signup = allow_guest_signup
        self.__provider.secret_key_private = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=64))
        self.__provider.secret_key_public = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32))
        self.__provider.save()

        return self.get_content()

    def get_content(self) -> dict:
        return {
            'id': str(self.__provider.pk),
            'name': self.__provider.name,
            'description': self.__provider.description,
            'administrators': self.__provider.administrators,
            'environments': self.__provider.environments,
            'secret_key_private': self.__provider.secret_key_private,
            'secret_key_public': self.__provider.secret_key_public,
            'allow_guest_signup': self.__provider.allow_guest_signup,
            'deactivated': self.__provider.deactivated,
        }