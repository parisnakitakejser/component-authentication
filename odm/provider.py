from mongoengine import Document, EmbeddedDocument, EmbeddedDocumentField, StringField, DictField, ListField, BooleanField


class ProviderSettings(EmbeddedDocument):
    logo_url = StringField()
    site_url = StringField()
    site_ssl = BooleanField(default=False)

    privacy_prolicy_url = StringField()
    terms_of_service_url = StringField()
    cancel_url = StringField()
    accept_url = StringField()

    in_development = BooleanField(default=True)
    ipv4_whitelist = ListField(StringField())
    ipv6_whitelist = ListField(StringField())
    roles = ListField()

class Provider(Document):
    name = StringField(required=True)
    description = StringField()

    settings = EmbeddedDocumentField(ProviderSettings)
    environments = DictField()
    domains = ListField()
    administrators = ListField()

    secret_key_private = StringField(max_length=64)
    secret_key_public = StringField(max_length=32)

    allow_guest_signup = BooleanField(default=False)
    deactivated = BooleanField(default=False)
