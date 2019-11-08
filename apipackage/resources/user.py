from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from datetime import datetime
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_raw_jwt)

from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims, fresh_jwt_required, jwt_optional

from apipackage.models.user import UserModel
from apipackage.blacklist import BLACKLIST

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('password',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('lastname',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('firstname',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('othernames',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('phone',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('orgnaisionationame',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )
_user_parser.add_argument('country',
                          type=str,
                          required=True,
                          help="This field cannot be blank."
                          )

# login and logout parser args
_user_login_parser = reqparse.RequestParser()
_user_login_parser.add_argument('email',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )

_user_login_parser.add_argument('password',
                                type=str,
                                required=True,
                                help="This field cannot be blank."
                                )


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()
        notAdmin = 0
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")

        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400

        user = UserModel(data['email'],
                         data['password'],
                         data['lastname'],
                         data['firstname'],
                         data['othernames'],
                         data['phone'],
                         data['country'],
                         data['orgnaisionationame'],
                         date_time,
                         notAdmin)
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    def post(self):
        data = _user_login_parser.parse_args()

        user = UserModel.find_by_email(data['email'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.userid, fresh=True)
            refresh_token = create_refresh_token(user.userid)
            return {
                       'access_token': access_token,
                       'refresh_token': refresh_token
                   }, 200

        return {"message": "Invalid Credentials!"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class User(Resource):
    @jwt_required
    def get(cls, email):
        user = UserModel.find_by_email(email)
        if not user:
            return {'message': 'User Not Found'}, 404

        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        return user.json(), 200

    @jwt_required
    def delete(cls, email):
        user = UserModel.find_by_email(email)
        if not user:
            return {'message': 'User Not Found'}, 404

        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        user.delete_from_db()
        return {'message': 'User deleted successfully.'}, 200

    @jwt_required
    def put(self, email):
        data = _user_parser.parse_args()
        user = UserModel.find_by_email(email)

        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        if not user:
            return {'message': 'User Not Found'}, 404

        user.password = data['password']
        user.lastname = data['lastname']
        user.firstname = data['firstname']
        user.othernames = data['othernames']
        user.phone = data['phone']
        user.country = data['country']
        user.orgnaisionationame = data['orgnaisionationame']
        user.save_to_db()

        return user.json()


class UserList(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        users = [users.json() for users in UserModel.find_all()]
        return {'usersList': users}, 200


class UserMakeAdmin(Resource):
    @jwt_required
    def post(self, email):
        user = UserModel.find_by_email(email)

        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        if not user:
            return {'message': 'User Not Found'}, 404

        user.isAdmin = 1

        user.save_to_db()

        return {'message': 'User now has an Admin right'}, 200


class UserRemoveAdmin(Resource):
    @jwt_required
    def post(self, email):
        user = UserModel.find_by_email(email)

        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        if not user:
            return {'message': 'User Not Found'}, 404

        user.isAdmin = 0

        user.save_to_db()

        return {'message': 'User right Admin removed'}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
