from fastapi import APIRouter, Depends, HTTPException
from api.authentication import get_current_active_user as auth_required
from database import Session
from database.todo import list_todos, find_todo, create_todo_entry

router = APIRouter()


@router.get("/", dependencies=[Depends(auth_required)], status_code=200)
def get_todos():
    with Session() as session:
        todos = list_todos(session)
        return todos


@router.get("/{todo_id}")
def get_todo(todo_id):
    with Session() as session:
        todo = find_todo(session, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Item not found")

        return todo


@router.post("/")
def create_todo():
    with Session() as session:
        todo = create_todo_entry(session, request)  # use model/body from FastApi
        return todo


@router.put("/{todo_id}")
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


@router.delete("/{todo_id}")
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).one_or_none()
    if not todo: abort(404)

    db.session.delete(todo)
    db.session.commit()

    return generate_response("todo", todo)


@router.get('/hello_world', dependencies=[Depends(auth_required)], status_code=200)
def hello_world() -> dict:
    """
        Generic hello world function. TODO: make useful

        :return: status message
    """
    return {"message": "Hello world"}