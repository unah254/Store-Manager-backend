# module imports
from flask import Flask

from flask_restful import Resource, reqparse

from werkzeug.security import check_password_hash

from flask_jwt_extended import create_access_token


import datetime

# local imports

from .utils import Validators

class User:

    user_id = 1

    def __init__(self, email=None, password=None,
                 is_admin=None):

        self.email = email
        if password:
            self.password_hash = generate_password_hash(password)
        self.is_admin = is_admin
        self.id = User.user_id

        User.user_id += 1


    def get_by_email(self, email):
        for user in Users:
            if user.email == email:
                return user

class SignUp(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("password", type=str, required=True,
                        help="This field can not be left bank")

    def post(self):
        """ Create a new user"""
        data = SignUp.parser.parse_args()

        email = data["email"]
        password = data["password"]

        validate = validators.Validators()


        if not validate.valid_email(email):
            return {"message": "enter valid email"}, 400

        if not validate.valid_password(password):
            return {"message": "password should start with a capital letter and include a number"}, 400


        if User().fetch_by_email(email):
            return {"message": "user with {} already exists".format(email)}, 400

        user = User(email, password)

        user.add()

        return {"message": "user {} created successfully".format(email)}, 201


class Login(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("email", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("password", type=str, required=True,
                        help="This field can not be left bank")

    def post(self):
        data = Login.parser.parse_args()

        email = data["email"]
        password = data["password"]

        validate = validators.Validators()

        user = User().fetch_by_email(email)

        if not user:
            return {'message': 'user not found'}, 404

        if not check_password_hash(user.password_hash, password):
            return {'message': 'incorrect password'}, 401

        expires = datetime.timedelta(minutes=30)
        token = create_access_token(user.serialize(), expires_delta=expires)
        return {'token': token, 'message': 'successfully logged'}, 200