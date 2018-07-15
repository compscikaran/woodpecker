from flask import Flask
import datamodels as dm
from endpoints import login_bp, transactions_bp, blacklist, account_bp
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./woodpecker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

dm.db.init_app(app)
with app.app_context():
    dm.db.create_all()

app.register_blueprint(transactions_bp)
app.register_blueprint(login_bp)
app.register_blueprint(account_bp)
jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


if __name__ == '__main__':
    app.run()
