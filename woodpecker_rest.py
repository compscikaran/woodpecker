from flask import Flask
import datamodels as dm
from endpoints import login_bp, transactions_bp


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./woodpecker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dm.db.init_app(app)
with app.app_context():
    dm.db.create_all()

app.register_blueprint(transactions_bp)
app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run()
