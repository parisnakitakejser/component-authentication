from flask import render_template, request, redirect
from bson.objectid import ObjectId
from urllib.parse import urlencode
import logging

from library.account import Account

from odm.accessToken import AccessToken as OdmAccessToken
from odm.account import Account as OdmAccount
from odm.provider import Provider as OdmProvider


class FlaskForm:
    @staticmethod
    def sign_in():
        alert_show = False
        alert_class = ''
        alert_content = ''


        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')

            account = Account()
            account_verify, account_data = account.verify(email=email, password=password)

            if not account_verify:
                alert_show = True
                alert_class = 'alert-danger'
                alert_content = 'Login information is incorrect!'

            else:
                accessToken = OdmAccessToken.objects(access_token=request.args.get('access_token'))
                accessToken.update(**{
                    'set__account_id': account_data['id'],
                    'set__account_token': account_data['token']
                })

                if ObjectId(request.environ['provider']['id']) in account_data['providers']:
                    logging.info('provider found, prepare for return to pages statement')

                    provider = OdmProvider(pk=request.environ['provider']['id'])

                    if provider.settings.in_development:
                        logging.info('confirm access - provider is in development send to response-in-development pages')
                        return redirect(f'/form/response-in-development?{urlencode(request.args)}', code=302)

                    else:
                        logging.info('confirm access - sending back to rel= + site url')

                else:
                    logging.info('provider not found for this account, sending to confirm pages')
                    return redirect(f'/form/confirm-access?{urlencode(request.args)}', code=302)

        return render_template('form/sign-in.html', **{
            'alert_show': alert_show,
            'alert_class': alert_class,
            'alert_content': alert_content
        })

    @staticmethod
    def confirm_access():
        return render_template('form/confirm-access.html', **{
            'name': 'Hello world',
            'site_url': 'test.com'
        })

    @staticmethod
    def response_in_development():
        return render_template('form/test.html')
