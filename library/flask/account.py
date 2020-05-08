import os
import logging
from bson.json_util import dumps
from flask import Response, request
from passlib.hash import pbkdf2_sha512
from mongoengine import errors
import uuid
import jwt

from library.account import Account
from odm.account import Account as OdmAccount


class FlaskAccount:
    @staticmethod
    def create():
        json_data = request.get_json()
        logging.info('Prepare data for create a new account')

        try:
            account = OdmAccount()
            account.email = json_data['email']
            account.password = pbkdf2_sha512.hash(json_data['password'])
            account.token = str(uuid.uuid4())
            account.first_name = json_data['first_name']
            account.last_name = json_data['last_name']
            account.save()

            logging.info('Account created success')

        except errors.NotUniqueError:
            logging.info('E-mail already exists')

            return Response(dumps({
                'status': 'Bad Request',
                'msg': 'E-mail already exists'
            }), mimetype='text/json'), 400

        return Response(dumps({
            'status': 'OK',
        }), mimetype='text/json'), 200

    @staticmethod
    def update():
        pass

    @staticmethod
    def sign_in():
        logging.info('execute account sign in')

        email = request.args.get('email')
        password = request.args.get('password')

        account = Account()
        account_verify, account_data = account.verify(email=email, password=password)

        if account_verify:
            logging.info('Sign in authorized: login success')

            return Response(dumps({
                'status': 'OK',
                'token': account_data['token']
            }), mimetype='text/json'), 200

        else:
            logging.info('Sign in unauthorized: account not exists or password is wrong')

            return Response(dumps({
                'status': 'Unauthorized',
            }), mimetype='text/json'), 401

    @staticmethod
    def sign_out():
        pass
