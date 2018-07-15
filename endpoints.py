from flask import Blueprint
from flask import jsonify, request, make_response
import datamodels as dm
import middleware as bl

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/user/new', methods=['POST'])
def do_create_user():
    return bl.create_new_user(request.get_json())


@login_bp.route('/user/login', methods=['POST'])
def do_login_user():
    return bl.login_user_session(request.get_json())


@login_bp.route('/user/logout', methods=['GET'])
def do_logout_user():
    return bl.logout_user_session(request.get_json())


transactions_bp = Blueprint('transactions_bp', __name__)


@transactions_bp.route('/', methods=['GET'])
def is_working():
    new_entry = dm.Transaction()
    new_entry.account_no = 1234
    dm.db.session.add(new_entry)
    dm.db.session.commit()
    return jsonify({'msg': 'Working'})

