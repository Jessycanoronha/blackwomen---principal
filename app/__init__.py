import os
from flask import Flask
from extensions import db
from flask_cors import CORS
from config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) 

    db.init_app(app)

    CORS(app)

    from app.routes.routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    return app
