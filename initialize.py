from endpoints import transactions_bp, login_bp, account_bp
from flask_jwt_extended import JWTManager
from apscheduler.schedulers.background import BackgroundScheduler
from middleware import calculate_interest, recheck_balance
from endpoints import blacklist
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import datamodels as dm

def initialize_blueprints(app):
    app.register_blueprint(transactions_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(account_bp)


def initialize_jwt(app):
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist


def initialize_scheduler():
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(calculate_interest, 'interval', days=30)
    scheduler.add_job(recheck_balance, 'interval', minutes=60)


def load_config(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./woodpecker.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['PDF_PATH'] = 'statements/'


def initialize_admin(app):
    admin = Admin(app)
    admin.add_view(ModelView(dm.User, dm.db.session))
    admin.add_view(ModelView(dm.Account, dm.db.session))
    admin.add_view(ModelView(dm.Transaction, dm.db.session))