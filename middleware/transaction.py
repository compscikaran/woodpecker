import datamodels as dm
from flask import make_response, json


def new_deposit(input_data):
    try:
        account_no = input_data.get('account_no')
        userid = input_data.get('user_id')
        amount = input_data.get('amount')
        if account_no is None or amount is None:
            resp = make_response("", 400)
            resp.headers["custom-message"] = 'Incomplete Data'
            return resp
        account = dm.db.session.query(dm.Account)\
            .filter(dm.Account.account_no == account_no).one_or_none()
        if account is None:
            resp = make_response("", 404)
            resp.headers["custom-message"] = 'Account Not Found'
            return resp
        user = dm.db.session.query(dm.User)\
            .filter(dm.User.user_id == account.user_id).one_or_none()
        if user.user_id != userid:
            resp = make_response("", 401)
            resp.headers["custom-message"] = 'Unauthorized Access To Account'
            return resp
        transaction = dm.Transaction()
        transaction.account = account
        transaction.amount = amount
        transaction.transaction_type = 'Deposit'
        dm.db.session.add(transaction)
        account.balance += amount
        dm.db.session.commit()
        resp_data = json.dumps({
            'transaction_id': transaction.transaction_id
        })
        resp = make_response(resp_data, 200)
        return resp
    except (KeyError, TypeError):
        dm.db.session.rollback()
        resp = make_response("", 400)
        resp.headers["custom-message"] = 'Could Not Complete Transaction'
        return resp


def new_withdrawal(input_data):
    try:
        account_no = input_data.get('account_no')
        userid = input_data.get('user_id')
        amount = input_data.get('amount')
        if account_no is None or amount is None:
            resp = make_response("", 400)
            resp.headers["custom-message"] = 'Incomplete Data'
            return resp
        account = dm.db.session.query(dm.Account)\
            .filter(dm.Account.account_no == account_no).one_or_none()
        if account is None:
            resp = make_response("", 404)
            resp.headers["custom-message"] = 'Account Not Found'
            return resp
        user = dm.db.session.query(dm.User)\
            .filter(dm.User.user_id == account.user_id).one_or_none()
        if user.user_id != userid:
            resp = make_response("", 401)
            resp.headers["custom-message"] = 'Unauthorized Access To Account'
            return resp
        if amount > account.balance:
            resp = make_response("", 400)
            resp.headers["custom-message"] = 'Account Cannot Be Overdrawn'
            return resp
        transaction = dm.Transaction()
        transaction.account = account
        transaction.amount = amount
        transaction.transaction_type = 'Withdrawal'
        dm.db.session.add(transaction)
        account.balance -= amount
        dm.db.session.commit()
        resp_data = json.dumps({
            'transaction_id': transaction.transaction_id
        })
        resp = make_response(resp_data, 200)
        return resp
    except (KeyError, TypeError):
        dm.db.session.rollback()
        resp = make_response("", 400)
        resp.headers["custom-message"] = 'Could Not Complete Transaction'
        return resp
