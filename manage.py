# inspiration: https://github.com/tko22/flask-boilerplate/blob/master/manage.py

from flask_migrate import Migrate
from api import create_app
from api.database import database as db

app = create_app()
migrate = Migrate(app, db)

@app.cli.command("recreate-database")
def recreate_database():
    db.drop_all()
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    app.run()