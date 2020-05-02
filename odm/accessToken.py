from mongoengine import Document, ObjectIdField, StringField, DateTimeField


class AccessToken(Document):
    provider_id = ObjectIdField()
    access_token = StringField(min_length=128, max_length=128)

    expired_at = DateTimeField()
    updated_at = DateTimeField()
    created_at = DateTimeField()
