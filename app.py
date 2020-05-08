import logging
from flask import Flask

from library.flask.account import FlaskAccount
from library.flask.token import FlaskToken
from library.flask.session import FlaskSession
from library.flask.provider import FlaskProvider
from library.flask.form import FlaskForm

from middleware import AuthTokenCheck, DBConnect
from middleware.providerVerify import ProviderVerify

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.wsgi_app = ProviderVerify(app.wsgi_app)
app.wsgi_app = AuthTokenCheck(app.wsgi_app)
app.wsgi_app = DBConnect(app.wsgi_app)

app.add_url_rule('/account', view_func=FlaskAccount.create, endpoint='account_create', methods=['PUT'])
app.add_url_rule('/account', view_func=FlaskAccount.update, endpoint='account_update', methods=['POST'])
app.add_url_rule('/account/sign-in', view_func=FlaskAccount.sign_in, endpoint='account_sign_in', methods=['GET'])
app.add_url_rule('/account/sign-out', view_func=FlaskAccount.sign_out, endpoint='account_sign_out', methods=['GET'])

app.add_url_rule('/verify', view_func=FlaskToken.verify, endpoint='token_verify', methods=['GET'])
app.add_url_rule('/verify/access-token', view_func=FlaskToken.verify_access_token, endpoint='token_verify_access_token', methods=['GET'])

app.add_url_rule('/session', view_func=FlaskSession.get, endpoint='session_get', methods=['GET'])
app.add_url_rule('/session', view_func=FlaskSession.update, endpoint='session_update', methods=['POST'])

app.add_url_rule('/provider', view_func=FlaskProvider.create, endpoint='provider_create', methods=['PUT'])
app.add_url_rule('/provider', view_func=FlaskProvider.update, endpoint='provider_update', methods=['POST'])
app.add_url_rule('/provider', view_func=FlaskProvider.get, endpoint='provider_get', methods=['GET'])

app.add_url_rule('/form/sign-in', view_func=FlaskForm.sign_in, endpoint='form_sign_in', methods=['GET'])
app.add_url_rule('/form/sign-in', view_func=FlaskForm.sign_in, endpoint='form_sign_in', methods=['POST'])
app.add_url_rule('/form/confirm-access', view_func=FlaskForm.confirm_access, endpoint='form_confrim_access', methods=['GET'])
app.add_url_rule('/form/confirm-access', view_func=FlaskForm.confirm_access, endpoint='form_confrim_access', methods=['POST'])
app.add_url_rule('/form/response-in-development', view_func=FlaskForm.response_in_development, endpoint='form_response_in_development', methods=['GET'])

if __name__ == '__main__':
    app.run('0.0.0.0', '5000', debug=True)