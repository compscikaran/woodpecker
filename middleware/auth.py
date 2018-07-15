import hashlib
import datamodels as dm
from flask import make_response, json


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
        resp_data = json.dumps({
            'user_id': user_id
        })
        resp = make_response(resp_data, 200)
        return resp
    except (KeyError, TypeError):
        dm.db.session.rollback()
        resp = make_response("", 400)
        resp.headers["custom-message"] = 'Could not create user'
        return resp
