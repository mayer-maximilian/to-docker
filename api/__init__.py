from flask import Flask
from api.blueprints.todo import todo

def create_app():
    app = Flask(__name__)

    app.register_blueprint(todo, url_prefix="/api/v0.1/todos")

    return app