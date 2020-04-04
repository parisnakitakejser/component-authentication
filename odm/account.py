from mongoengine import Document, EmailField, StringField, ListField, BooleanField


class Account(Document):
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    token = StringField(required=True)

    administrator = BooleanField(default=False)
    deactivated = BooleanField(default=False)

    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

    providers = ListField(default=[])
