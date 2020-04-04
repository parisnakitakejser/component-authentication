import logging
from flask import Flask

from library.flask.account import FlaskAccount
from middleware import AuthTokenCheck, DBConnect

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.wsgi_app = AuthTokenCheck(app.wsgi_app)
app.wsgi_app = DBConnect(app.wsgi_app)

app.add_url_rule('/account', view_func=FlaskAccount.create, methods=['PUT'])
app.add_url_rule('/account', view_func=FlaskAccount.update, methods=['POST'])
app.add_url_rule('/account/sign-in', view_func=FlaskAccount.sign_in, methods=['GET'])
app.add_url_rule('/account/sign-out', view_func=FlaskAccount.sign_out, methods=['GET'])

if __name__ == '__main__':
    app.run('0.0.0.0', '5000', debug=True)