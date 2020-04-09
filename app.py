import logging
from flask import Flask

from library.flask.account import FlaskAccount
from library.flask.token import FlaskToken
from library.flask.session import FlaskSession
from middleware import AuthTokenCheck, DBConnect

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.wsgi_app = AuthTokenCheck(app.wsgi_app)
app.wsgi_app = DBConnect(app.wsgi_app)

app.add_url_rule('/account', view_func=FlaskAccount.create, endpoint='account_create', methods=['PUT'])
app.add_url_rule('/account', view_func=FlaskAccount.update, endpoint='account_update', methods=['POST'])
app.add_url_rule('/account/sign-in', view_func=FlaskAccount.sign_in, endpoint='account_sign_in', methods=['GET'])
app.add_url_rule('/account/sign-out', view_func=FlaskAccount.sign_out, endpoint='account_sign_out', methods=['GET'])

app.add_url_rule('/verify', view_func=FlaskToken.verify, endpoint='token_verify', methods=['GET'])

app.add_url_rule('/session', view_func=FlaskSession.get, endpoint='session_get', methods=['GET'])
app.add_url_rule('/session', view_func=FlaskSession.update, endpoint='session_update', methods=['GET'])

if __name__ == '__main__':
    app.run('0.0.0.0', '5000', debug=True)