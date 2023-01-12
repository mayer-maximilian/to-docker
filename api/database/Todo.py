from .database import database as db


class Todo(db.Model):

    __tablename__ = "todo"

    id          = db.Column(db.Integer, unique=True, primary_key=True)
    title       = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    deadline    = db.Column(db.String)
    done        = db.Column(db.Boolean)

    def __init__(self, title: str, description: str = None, deadline: str = None, done: bool = False) -> None:
        super().__init__()

        self.title       = title
        self.description = description
        self.deadline    = deadline
        self.done        = done

    def to_dict(self):
        return {
            "id":          self.id,
            "title":       self.title,
            "description": self.description,
            "deadling":    self.deadline,
            "done":        "true" if self.done else "false"
        }

    def __repr__(self) -> str:
        return f"<Todo {self.title}>"

