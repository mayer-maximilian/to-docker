# inspired by https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

from flask import Blueprint, request, jsonify, abort, make_response

todo = Blueprint("todo", __name__)

resources = [
    {
        "id": 1,
        "title": "Buy Milk",
        "description": "Go to the store and by some milk",
        "deadline": "today",
        "status": "open"
    },
    {
        "id": 2,
        "title": "Clean Kitchen",
        "description": "Go to the store and by some milk",
        "deadline": "tomorrow",
        "status": "open"
    }
]

def create_todo_data(request):

    json = request.json

    if not json or not "title" in json:
        return None

    todo = {
        "id": resources[-1]["id"] + 1,
        "title": json["title"],
        "description": json.get("description", ""),
        "deadline": json.get("deadline", None),
        "status": "open"
    }

    resources.append(todo)
    return todo


@todo.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Resource not found'}), 404)


@todo.route("/", methods=["GET"])
def get_todos():
    return jsonify({"todos": resources})


@todo.route("<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    try:
        todo = next(todo for todo in resources if todo["id"] == todo_id)
    except:
        abort(404)
        
    return jsonify({"todo": todo})


@todo.route("/", methods=["POST"])
def create_todo():
    todo = create_todo_data(request)
    if not todo: abort(404)
    return jsonify({"todo": todo}), 201


@todo.route("<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):

    json = request.json

    if not json: abort(404)

    try:
        todo = next(todo for todo in resources if todo["id"] == todo_id)

        def update_attribute(attribute_name):
            todo[attribute_name] = json.get(attribute_name, todo[attribute_name])

        update_attribute("title")
        update_attribute("description")
        update_attribute("deadline")
        update_attribute("status")
    except:
        todo = create_todo_data(request)
        if not todo: abort(404)

    return jsonify({"todo": todo})


@todo.route("<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    try:
        todo = next(todo for todo in resources if todo["id"] == todo_id)
    except:
        abort(404)
    resources.remove(todo)
    return jsonify({'result': True})