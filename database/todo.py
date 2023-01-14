from fastapi import HTTPException
from sqlalchemy import Column, String, Integer, Boolean

from pydantic import BaseModel
from database.database import Base


class UserNotFoundException(HTTPException):
    """The exception that is thrown when the give user doesn't exist"""
    def __init__(self, message='User not found'):
        super().__init__(status_code=404, detail=message)


class TodoModel(BaseModel):

    title: str
    description: str = None
    deadline: str = None
    done: bool = False

    def to_database(self, session):
        todo = Todo(title       = self.title,
                    description = self.description,
                    deadline    = self.deadline,
                    done        = self.done)

        session.add(todo)
        session.commit()

        return todo.__dict__

class Todo(Base):
    """ORM class for the todos"""
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    deadline = Column(String)
    done = Column(Boolean)


def list_todos(session):
    todos = session.query(Todo).all()
    return [todo.__dict__ for todo in todos]


def find_todo(session, todo_id):
    todo = session.query(Todo).filter(Todo.id==todo_id).one_or_none()
    return todo.__dict__ if todo else None


def create_todo_entry(session, title, description=None, deadline=None, done=False):
    todo = Todo(title=title, description=description, deadline=deadline, done=done)
    msg = 'TODO created'

    session.add(todo)
    session.commit()

    return msg
