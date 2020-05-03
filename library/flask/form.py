from flask import render_template, request

from library.account import Account


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
                alert_show = True
                alert_class = 'alert-success'
                alert_content = 'Login success'

        return render_template('form/sign-in.html', **{
            'alert_show': alert_show,
            'alert_class': alert_class,
            'alert_content': alert_content
        })