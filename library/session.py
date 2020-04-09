import os
import hashlib
import uuid
import logging
from mongoengine import DoesNotExist
from bson.objectid import ObjectId
from datetime import datetime, timedelta
from typing import Union

from odm.session import Session as OdmSession, session_lifetime


class Session:
    @staticmethod
    def generate():
        secret_key = os.getenv('SESSION_SECRET_KEY')
        uuid_v4 = str(uuid.uuid4())
        session_id = hashlib.sha512(f'{uuid_v4}{secret_key}'.encode('utf-8')).hexdigest()

        logging.info(f'session id generated: {session_id}')

        return session_id

    @staticmethod
    def get(account_id: str, session_id: Union[str, None]) -> (Union[str, None], Union[str, None]):
        if session_id:
            try:
                account_session = OdmSession.objects.get(session_id=session_id, expires_at__gte=datetime.utcnow())
                if account_session.account_id != ObjectId(account_id):
                    return None, None

                session_data = account_session.session_data

                account_session.updated_at = datetime.utcnow()
                account_session.expires_at = datetime.utcnow() + timedelta(seconds=session_lifetime)
                account_session.save()

            except DoesNotExist:
                logging.info(f'session not exists or expires, create new session for account_id: {account_id}')

                session_id = Session.create(account_id=account_id)
                session_data = {}
        else:
            logging.info(f'session not exists, create new session for account_id: {account_id}')

            session_id = Session.create(account_id=account_id)
            session_data = {}

        return session_id, session_data

    @staticmethod
    def create(account_id: str) -> str:
        logging.info(f'create session for account: {account_id}')

        session_id = Session.generate()

        session = OdmSession(session_id=session_id, account_id=account_id)
        session.created_at = datetime.utcnow()
        session.expires_at = datetime.utcnow() + timedelta(seconds=session_lifetime)
        session.save()

        return session_id

    @staticmethod
    def update(account_id: str, session_id: str, session_data: dict) -> (Union[dict, None], Union[str, None]):
        session_id, _ = Session.get(account_id=account_id, session_id=session_id)

        if session_id is not None:
            logging.info(f'update session data for account: {account_id} in session: {session_id} is updated')

            account_session = OdmSession.objects.get(account_id=account_id, session_id=session_id)
            account_session.session_data = session_data
            account_session.expires_at = datetime.utcnow() + timedelta(seconds=session_lifetime)
            account_session.updated_at = datetime.utcnow()
            account_session.save()

            return session_id, session_data
        else:
            logging.info(f'account: {account_id} did not have access for this session: {session_id}')

            return None, None
