# inspired by https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

from flask import Blueprint, request, jsonify, abort, make_response
from api.database import Todo, database as db
from api.utils import generate_response, generate_list_response

todo = Blueprint("todo", __name__)


def create_todo_entry(request):

    json = request.json

    if not json or not "title" in json:
        return None

    todo = Todo(json["title"], 
                json.get("description", ""), 
                json.get("deadline", None), 
                json.get("done", "false") == "true")

    db.session.add(todo)
    db.session.commit()

    return todo


@todo.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


@todo.route("/", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return generate_list_response("todos", todos)


@todo.route("<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).one_or_none()
    if not todo: abort(404)
    return generate_response("todo", todo)


@todo.route("/", methods=["POST"])
def create_todo():
    todo = create_todo_entry(request)
    if not todo: abort(404)
    return generate_response("todo", todo), 201


@todo.route("<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):

    json = request.json
    if not json: abort(404)

    todo = Todo.query.filter_by(id=todo_id).one_or_none()

    if todo:
        try:
            
            todo.title = json.get("title", todo.title)
            todo.description = json.get("description", todo.description)
            todo.deadline = json.get("deadline", todo.deadline)
            todo.done = json.get("done", todo.done) == "true"

            db.session.commit()

        except Exception as e:
            print(e)
            abort(404)
    else:
        todo = create_todo_entry(request)
        if not todo: abort(404)

    return generate_response("todo", todo)


@todo.route("<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).one_or_none()
    if not todo: abort(404)

    db.session.delete(todo)
    db.session.commit()

    return generate_response("todo", todo)