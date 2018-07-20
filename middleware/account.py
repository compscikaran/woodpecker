import datamodels as dm
from flask import make_response, json


def create_bank_account(input_data):
    try:
        userid = input_data.get('user_id')
        rate = input_data.get('aer')
        user = dm.db.session.query(dm.User) \
            .filter(dm.User.user_id == userid).one_or_none()
        if user is None:
            resp = ("", 404)
            resp.headers["custom-message"] = 'User Not Found'
            return resp
        account = dm.Account()
        account.user = user
        account.aer = rate
        dm.db.session.add(account)
        dm.db.session.commit()
        resp_data = json.dumps({
            'user_id': userid,
            'account_no': account.account_no
        })
        resp = make_response(resp_data, 200)
        return resp
    except (KeyError, TypeError):
        dm.db.session.rollback()
        resp = make_response("", 400)
        resp.headers["custom-message"] = 'Account Could Not Be Created'
        return resp
