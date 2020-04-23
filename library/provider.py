from typing import Union
import random
import string

from odm.provider import Provider as OdmProvider


class Provider:
    administrators = []

    def __init__(self, provider_id: Union[str, None] = None):
        if provider_id is not None:
            pass
        else:
            self.__provider = OdmProvider()

    def create(self, name: str, allow_guest_signup: bool) -> dict:
        self.__provider.name = name
        self.__provider.allow_guest_signup = allow_guest_signup
        self.__provider.secret_key_private = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=64))
        self.__provider.secret_key_public = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=32))
        self.__provider.save()

        return {

        }