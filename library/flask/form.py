from flask import render_template


class FlaskForm:
    @staticmethod
    def sign_in():
        return render_template('form/sign-in.html')