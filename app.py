import os

from flask import Flask
from flask_migrate import Migrate

from utils.models import db

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({'status': True})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)



if __name__ == "__main__":
    app.run(debug=True)