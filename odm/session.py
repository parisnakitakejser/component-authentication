import os
from mongoengine import Document, StringField, ObjectIdField, DictField, IntField, DateTimeField

session_lifetime = int(os.getenv('SESSION_LIFETIME')) if os.getenv('SESSION_LIFETIME') is not None else (60*60*24*7)


class Session(Document):
    session_id = StringField(required=True)
    account_id = ObjectIdField(required=True)
    session_data = DictField(default={})
    provider = ObjectIdField()

    created_at = DateTimeField(required=True)
    updated_at = DateTimeField()
    expires_at = DateTimeField(required=True)