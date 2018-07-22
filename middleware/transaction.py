import datamodels as dm
from flask import make_response, json, send_from_directory
import pandas as pd
import pdfkit as pk
import datetime as dt

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


def fetch_transactions(account_no):
    try:
        account = dm.db.session.query(dm.Account)\
            .filter(dm.Account.account_no == account_no).one_or_none()
        if account is None:
            resp = make_response("", 404)
            resp.headers["custom-message"] = 'Account Not Found'
            return resp
        transactions = dm.db.session.query(dm.Transaction)\
            .filter(dm.Transaction.account_no == account_no).all()
        return_dict = {
            'account_no': account.account_no,
            'user_id': account.user_id,
            'balance': account.balance,
            'aer': account.aer,
            'created_date': account.timestamp,
            'transactions': []
        }
        for transaction in transactions:
            return_dict['transactions'].append({
                'transaction_id': transaction.transaction_id,
                'amount': transaction.amount,
                'type': transaction.transaction_type,
                'datetime': transaction.timestamp})
        res = json.dumps(return_dict)
        resp = make_response(res, 200)
        return resp
    except (KeyError, TypeError):
        resp = make_response("", 400)
        resp.headers["custom-message"] = 'Invalid Data Request'
        return resp

def create_pdf(account_no):
    try:
        account = dm.db.session.query(dm.Account)\
            .filter(dm.Account.account_no == account_no).one_or_none()
        if account is None:
            resp = make_response("", 404)
            resp.headers["custom-message"] = 'Account Not Found'
            return resp
        transactions = dm.db.session.query(dm.Transaction.timestamp, dm.Transaction.amount, dm.Transaction.timestamp, dm.Transaction.transaction_type)\
            .filter(dm.Transaction.account_no == account_no).all()
        df_all = pd.DataFrame(transactions)
        html = df_all.to_html()
        filename = str(dt.datetime.now()) + str(account_no) + '.pdf'
        filepath = 'statements/'+ filename
        pk.from_string(html, filepath)
        return send_from_directory('statements',filepath)
    except (KeyError, TypeError):
        resp = make_response("", 400)
        resp.headers["custom-message"] = 'Invalid Data Request'
        return resp


