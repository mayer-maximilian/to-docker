# inspiration: https://github.com/tko22/flask-boilerplate/blob/master/manage.py

from api import create_app
from api.database import database as db

app = create_app()

@app.cli.command("create-database")
def create_database():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run()