import hashlib
import datamodels as dm
from flask import make_response, json
from flask_jwt_extended import create_access_token, create_refresh_token


def create_new_user(input_data):
    try:
        username = input_data.get('username')
        password = input_data.get('password')
        email = input_data.get('email')
        if username is None or password is None or email is None:
            resp = make_response("", 400)
            resp.headers["custom-message"] = 'Incomplete Data'
            return resp
        hash_pass = hashlib.sha256(password.encode()).hexdigest()
        new_user = dm.User()
        new_user.password = hash_pass
        new_user.user_name = username
        new_user.email = email
        dm.db.session.add(new_user)
        dm.db.session.commit()
        user_id = new_user.query.with_entities(dm.User.user_id).order_by(dm.User.user_id.desc()).first()[0]
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        resp_data = json.dumps({
            'user_id': user_id,
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        resp = make_response(resp_data, 200)
        return resp
    except (KeyError, TypeError):
        dm.db.session.rollback()
        resp = make_response("", 400)
        resp.headers["custom-message"] = 'Could not create user'
        return resp


def login_user_session(input_data):
    try:
        username = input_data.get('username')
        password = input_data.get('password')
        current_user = dm.db.session.query(dm.User)\
                            .filter(dm.User.user_name == username).one_or_none()
        if not current_user:
            resp = make_response("", 404)
            resp.headers["custom-message"] = 'User Not Found'
            return resp
        if current_user.password ==  hashlib.sha256(password.encode()).hexdigest():
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
        else:
            resp = make_response("", 400)
            resp.headers["custom-message"] = 'Incorrect Password'
            return resp
        resp_data = json.dumps({
            'user_id': current_user.user_id,
            'access_token': access_token,
            'refresh_token': refresh_token
        })
        resp = make_response(resp_data, 200)
        return resp
    except (KeyError, TypeError):
        resp = make_response("", 400)
        resp.headers["custom-message"] = 'Invalid Request'
        return resp
