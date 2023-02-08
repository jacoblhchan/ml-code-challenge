from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from src.blueprints.sentiment import sentiment_blueprint
from src.blueprints.root import root_blueprint
from src.models import db

migrate = Migrate()


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # DO NOT deploy this application to a production environment without first adjusting
    # the CORS settings
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Initialize blueprints
    app.register_blueprint(root_blueprint)
    app.register_blueprint(sentiment_blueprint)

    return app
