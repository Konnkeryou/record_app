from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from record_app import controllers

db = SQLAlchemy()

def create_app():

    app = Flask (__name__)

    app.config.from_object("config.app_config")

    db.init_app()

    from controllers import registerable_controlers
    for controlller in registerable_controlers:
        app.register_blueprint(controlller)

    return app 
