from flask import render_template


class FlaskForm:
    @staticmethod
    def sign_in():
        alert_show = False
        alert_class = ''
        alert_content = ''

        # alert_show = True
        # alert_class = 'alert-danger'
        # alert_content = 'Login information is incorrect!'


        return render_template('form/sign-in.html', **{
            'alert_show': alert_show,
            'alert_class': alert_class,
            'alert_content': alert_content
        })