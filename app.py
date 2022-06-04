import os

from flask import Flask
from flask_migrate import Migrate

from api_views.auth import auth
from api_views.users import user_data
from utils.models import db

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth)
app.register_blueprint(user_data)


if __name__ == "__main__":
    app.run(debug=True)