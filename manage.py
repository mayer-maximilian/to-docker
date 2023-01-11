# inspiration: https://github.com/tko22/flask-boilerplate/blob/master/manage.py

from api import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True,)