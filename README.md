# to-docker
A super basic to-do list application designed to be deployed with Docker, splitting the frontend, backend, and database in a seperate container each.

# Setup
Before you can start, you need to install the Python requirements listed in `requirements.txt` using the command `pip install -r requirements.txt`.

# Execution
First, start the postgres database, which runs in a Docker container. This is done through `docker compose`, and the coresponding configuration file is part of this directory. So you can just run `docker compose up`. If you want to reset the content in the database, execute `flask --app ./manage.py recreate-database` while the Docker container is running. The volume used for the database is persistant and will remain intact inbetween database runs.

The API is currently not containerized, so you need to just run it on the command line. It will connect to the database via localhost. You can run the API by calling `flask --app ./manage.py --debug run` or by directly executing the `manage.py` file.

You can test the API in a browser such as Firefox. However, you will only receive JSON responses. A proper interface is still missing.

# Next Steps
    - Containerize the API
    - Build a frontend
    - Properly configure 
