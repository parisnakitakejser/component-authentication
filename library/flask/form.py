from flask import render_template, request, redirect
from bson.objectid import ObjectId
from urllib.parse import urlencode
import logging

from library.account import Account
from library.provider import Provider

from odm.accessToken import AccessToken as OdmAccessToken
from odm.account import Account as OdmAccount
from odm.provider import Provider as OdmProvider


class FlaskForm:
    @staticmethod
    def sign_in():
        alert_show = False
        alert_class = ''
        alert_content = ''

        provider = OdmProvider.objects.get(pk=request.environ['provider']['id'])

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

                    if provider.settings.in_development:
                        logging.info('confirm access - provider is in development send to response-in-development pages')
                        return redirect(f'/form/response-in-development?{urlencode(request.args)}', code=302)

                    else:
                        provider = Provider(provider_id=request.environ['provider']['id'])

                        logging.info('confirm access - sending back to rel= + site url')
                        return redirect(provider.get_accept_return_url(args=dict(request.args)))

                else:
                    logging.info('provider not found for this account, sending to confirm pages')
                    return redirect(f'/form/confirm-access?{urlencode(request.args)}', code=302)

        return render_template('form/sign-in.html', **{
            'alert_show': alert_show,
            'alert_class': alert_class,
            'alert_content': alert_content,
            'guest_signup': provider.allow_guest_signup,
            'args': f'{urlencode(request.args)}'
        })

    @staticmethod
    def confirm_access():
        provider = OdmProvider.objects.get(pk=request.environ['provider']['id'])

        if request.method == 'POST':
            if request.form.get('btn-trigger') == 'cancel':
                print('do what we want with cancel')

            elif request.form.get('btn-trigger') == 'accept':
                accessToken = OdmAccessToken.objects.get(access_token=request.args.get('access_token'))

                OdmAccount.objects(pk=accessToken.account_id).update(**{
                    'push__providers': request.environ['provider']['id']
                })

                if provider.settings.in_development:
                    logging.info('account grant access for provider - its in development mode, sending for reponse-in-development pages')
                    return redirect(f'/form/response-in-development?{urlencode(request.args)}')

                else:
                    provider = Provider(provider_id=request.environ['provider']['id'])
                    logging.info('account grant access for provider - return to rel or accept url for this provider')
                    return redirect(provider.get_accept_return_url(args=dict(request.args)))

            else:
                logging.info('Wrong btn-trigger command hitten!!!')

        return render_template('form/confirm-access.html', **{
            'name': provider.name,
            'site_url': provider.settings.site_url
        })

    @staticmethod
    def response_in_development():
        provider = Provider(provider_id=request.environ['provider']['id'])

        return render_template('form/response-in-development.html', **{
            'site_url': provider.get_accept_return_url(args=dict(request.args))
        })

    @staticmethod
    def sign_up():
        provider = Provider(provider_id=request.environ['provider']['id'])

        msg = []
        resp = True

        provider = OdmProvider.objects.get(pk=request.environ['provider']['id'])

        if request.method == 'POST' and provider.allow_guest_signup:
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            password = request.form.get('password')
            password_confirm = request.form.get('password_confirm')

            account = Account()
            resp, msg, url_redirect, status_code = account.create(data={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
                'password_confirm': password_confirm,
            }, sign_in=True, access_token=request.args.get('access_token'), url_args=dict(request.args))

            if resp:
                return redirect(url_redirect, code=status_code)

        return render_template('form/sign-up.html', **{
            'args': urlencode(dict(request.args)),
            'guest_signup': provider.allow_guest_signup,
            'resp': resp,
            'msg': '<br />'.join(msg)
        })

    @staticmethod
    def reset_password():
        provider = Provider(provider_id=request.environ['provider']['id'])

        return render_template('form/reset-password.html', **{
            'args': urlencode(dict(request.args))
        })
