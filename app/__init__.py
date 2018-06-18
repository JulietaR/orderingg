from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
# fixF401 from flask_migrate import Migrate
from app.routes import rest

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
# fixF841    migrate = Migrate(app, db)
    app.register_blueprint(rest)

# fixF401 from app import models

    return app
