# to-docker
A super basic to-do list application designed to be deployed with Docker, splitting the frontend, backend, and database in a seperate container each.

# Execution Hints
The current version only supports to run a postgres database in a Docker container, while the API itself has to be run on the command line using `flask --app ./manage.py --debug run` or by directly executing the `manage.py` file. The app is configured to connect to the postgres database on localhost.

The postgres database can be started by executing `docker compose up`. If you want to reset the content in the database, execute `flask --app ./manage.py recreate-database` while the Docker container is running. The volume used for the database is persistant and will remain intact inbetween database runs.

# Next Steps
    - Containerize the API
    - Build a frontend
    - Properly configure 
