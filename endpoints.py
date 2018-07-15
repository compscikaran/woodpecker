from flask import Blueprint
from flask import jsonify, request
import datamodels as dm
import middleware as bl

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/user/new', methods=['POST'])
def new_user():
    return bl.create_new_user(request.get_json())


transactions_bp = Blueprint('transactions_bp', __name__)


@transactions_bp.route('/', methods=['GET'])
def is_working():
    new_entry = dm.Transaction()
    new_entry.account_no = 1234
    dm.db.session.add(new_entry)
    dm.db.session.commit()
    return jsonify({'msg': 'Working'})

