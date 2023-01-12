from flask import Flask
from api.config import Config
from api.database import database as db
from api.blueprints.todo import todo

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(todo, url_prefix="/api/v0.1/todos")

    return app