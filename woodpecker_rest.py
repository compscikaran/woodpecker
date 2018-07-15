from flask import Flask
from datamodels.db import db
from endpoints import transactions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./woodpecker.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(transactions)

if __name__ == '__main__':
    app.run(debug=True)
