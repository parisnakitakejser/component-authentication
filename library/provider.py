from typing import Union
import random
import string
import logging
from urllib.parse import urlencode
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

    def __construction(self, fields: dict) -> (Union[bool, None], list):
        response = True
        validation = []

        if len(fields) > 0:
            if 'name' in fields:
                if isinstance(fields['name'], str):
                    self.__provider.name = fields['name']
                else:
                    response = False
                    validation.append('name need to be str type')

            if 'description' in fields:
                if isinstance(fields['description'], str):
                    self.__provider.description = fields['description']
                else:
                    response = False
                    validation.append('description need to be str type')

            if 'allow_guest_signup' in fields:
                if isinstance(fields['allow_guest_signup'], bool):
                    self.__provider.allow_guest_signup = fields['allow_guest_signup']
                else:
                    response = False
                    validation.append('allow_guest_signup need to be bool type')

            if 'deactivated' in fields:
                if isinstance(fields['deactivated'], bool):
                    self.__provider.deactivated = fields['deactivated']
                else:
                    response = False
                    validation.append('deactivated need to be bool type')

        else:
            response = False
            validation.append('must be at least 1 field')

        return response, validation

    def update(self, fields: dict) -> (Union[bool, None], list):
        response, validation = self.__construction(fields=fields)

        if response:
            self.__provider.save()

        return response, validation

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

    def get_accept_return_url(self, args: dict) -> str:
        if 'rel' in args:
            response_url = args['rel']
            del args['rel']

        else:
            response_url = self.__provider.settings.accept_url

        response_url = response_url if response_url is not None else ''

        url_prefix = 'https://' if self.__provider.settings.site_ssl else 'http://'
        site_url = self.__provider.settings.site_url

        return f'{url_prefix}{site_url}{response_url}?{urlencode(args)}'
