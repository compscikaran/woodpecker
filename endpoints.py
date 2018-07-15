from flask import Blueprint
from flask import jsonify
import datamodels as dm

transactions = Blueprint('transactions', __name__)


@transactions.route('/', methods=['GET'])
def is_working():
    new_entry = dm.Transaction()
    new_entry.account_no = 1234
    dm.db.session.add(new_entry)
    dm.db.session.commit()
    return jsonify({'msg': 'Working'})
