from flask import Blueprint
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from flask_jwt_extended import jwt_refresh_token_required, create_access_token
import middleware as bl

blacklist = set()

login_bp = Blueprint('login_bp', __name__)


@login_bp.route('/user/new', methods=['POST'])
def do_create_user():
    return bl.create_new_user(request.get_json())


@login_bp.route('/user/login', methods=['POST'])
def do_login_user():
    return bl.login_user_session(request.get_json())


@login_bp.route('/user/logout', methods=['GET'])
@jwt_required
def do_logout_access():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@login_bp.route('/user/logout_refresh', methods=['GET'])
@jwt_refresh_token_required
def do_logout_refresh():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@login_bp.route('/user/token', methods=['GET'])
@jwt_refresh_token_required
def refresh_access_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    return jsonify({'access_token': access_token})


account_bp = Blueprint('account_bp', __name__)


@account_bp.route('/account/new', methods=['POST'])
@jwt_required
def create_account():
    return bl.create_bank_account(request.get_json())


transactions_bp = Blueprint('transactions_bp', __name__)


@transactions_bp.route('/transaction/deposit', methods=['POST'])
@jwt_required
def do_deposit():
    return bl.new_deposit(request.get_json())


@transactions_bp.route('/transaction/withdrawal', methods=['POST'])
@jwt_required
def do_withdrawal():
    return bl.new_withdrawal(request.get_json())


@transactions_bp.route('/transaction/interest', methods=['GET'])
@jwt_required
def do_deposit_interest():
    bl.calculate_interest()
    return jsonify({'msg': 'Interest Calculation Successful'})


@transactions_bp.route('/transaction/fetch', methods=['GET'])
@jwt_required
def do_fetch_transactions():
    account_no = request.args.get('account_no')
    if account_no is None:
        return jsonify({'msg': 'Please Specify Account Number'})
    return bl.fetch_transactions(account_no)

@transactions_bp.route('/transaction/statement', methods=['GET'])
@jwt_required
def do_fetch_statement():
    account_no = request.args.get('account_no')
    if account_no is None:
        return jsonify({'msg': 'Please Specify Account Number'})
    return bl.create_pdf(account_no)

