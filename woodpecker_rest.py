from flask import Flask
from initialize import initialize_blueprints, initialize_jwt, initialize_scheduler, load_config
import datamodels as dm

app = Flask(__name__)
load_config(app)
dm.db.init_app(app)
with app.app_context():
    dm.db.create_all()
initialize_blueprints(app)
initialize_jwt(app)
initialize_scheduler()

if __name__ == '__main__':
    app.run()
