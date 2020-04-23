from mongoengine import Document, StringField, DictField, ListField, BooleanField


class Provider(Document):
    name = StringField(required=True)
    description = StringField()
    environments = DictField()
    domains = ListField()
    administrators = ListField()
    secret_key_private = StringField(max_length=64)
    secret_key_public = StringField(max_length=32)
    allow_guest_signup = BooleanField(default=False)
    deactivated = BooleanField(default=False)
