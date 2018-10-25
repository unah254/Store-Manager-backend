# module imports
import datetime
from flask_restful import Resource, reqparse

from functools import wraps
from werkzeug.security import check_password_hash

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# local imports
from .models import User, Users
from .utils import Validators




def admin_only(_f):
    ''' Restrict access if not admin '''
    @wraps(_f)
    def wrapper_function(*args, **kwargs):
        user = User().fetch_by_email(get_jwt_identity())

        print(user)

        if not user.admin:
            return {'message': 'Anauthorized access, you must be an admin to access this level'}, 401
        return _f(*args, **kwargs)
    return wrapper_function

def user_only(_f):
    ''' Restrict access if not attendant '''
    @wraps(_f)
    def wrapper_function(*args, **kwargs):
        user = User().fetch_by_email(get_jwt_identity())

        if user.admin:
            return {'message': 'Anauthorized access, you must be an attendant to access this level'}, 401
        return _f(*args, **kwargs)
    return wrapper_function

class SignUp(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument("email", type=str, required=True,
                        help="This field can not be left bank")
    parser.add_argument("password", type=str, required=True,
                        help="This field can not be left bank")
    

    @jwt_required
    @admin_only
    def post(self):
        """ Create a new user"""
        data = SignUp.parser.parse_args()

        email = data["email"]
        password = data["password"]
        

        validate = Validators()


        if not validate.valid_email(email):
            return {"message": "enter valid email"}, 400

        if not validate.valid_password(password):
            return {"message": "password should start with a capital letter and include a number"}, 400


        if User().fetch_by_email(email):
            return {"message": "user with {} already exists".format(email)}, 400

        user = User(email, password)
        Users.append(user)

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

        user = User().fetch_by_email(email)

        if user and check_password_hash(user.password_hash, password):
            expires = datetime.timedelta(days=2)
            token = create_access_token(user.email, expires_delta=expires)
            return {'token': token, 'message': 'successfully logged'}, 200
        return {'message': 'user not found'}, 404
    
