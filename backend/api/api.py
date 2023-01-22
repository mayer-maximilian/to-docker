from fastapi import APIRouter, Depends, HTTPException
from api.authentication import get_current_active_user as auth_required
from database import Session
from database.todo import TodoModel, search_todo, list_todos, find_todo

router = APIRouter(prefix="/api")


@router.get("/", dependencies=[Depends(auth_required)], status_code=200)
def get_todos():
    with Session() as session:
        todos = list_todos(session)
        return todos

@router.get("/{todo_id}")
def get_todo(todo_id: int):
    with Session() as session:
        todo = find_todo(session, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Item not found")
        return todo

@router.post("/")
def create_todo(todo: TodoModel):
    # TODO: Return is empty, as Todo object is cleared after it is added to database
    with Session() as session:
        return todo.to_database(session)

@router.put("/{todo_id}")
def update_todo(todo_id: int, todo_update: TodoModel):
    with Session() as session:
        todo = search_todo(session, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Item not found")

        if todo_update.title:       todo.title       = todo_update.title
        if todo_update.description: todo.description = todo_update.description
        if todo_update.deadline:    todo.deadline    = todo_update.deadline
        if todo_update.done:        todo.done        = todo_update.done

        session.commit()

        return find_todo(session, todo_id)

@router.delete("/{todo_id}")
def delete_todo(todo_id):
    with Session() as session:
        todo = search_todo(session, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Item not found")
        
        session.delete(todo)
        session.commit()

        return todo.__dict__
