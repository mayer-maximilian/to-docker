# Kubernetified Todo-App

## Table of Contents

* [About the Project](#about-the-project)
* [Contributors](#contributors)
* [Web Application](#Web Application)
* [Azure Configuration](#Azure Configuration)
* [Docker Components](#Docker Components)
* [Kubernetes Components](#Kubernetes Components)
* [Helm](#Helm)
* [Setup](#Setup)
* [Execution](#Execution)
* [Scaling and Updating](#Scaling and Updating)

# About the Project
This project was completed for the course Software Containerization 2023 at Vrije Universteit Amsterdam. It is A super basic to-do list application designed to be be easily deployed by anyone using Helm. Each component of the application (frontent, api, database, redis) are implemented using kubernetes components, docker images and containers in the scheme outlined below. Our implementation is deployed in an Azure environment.

![alt text](https://github.com/Xantocx/to-docker/blob/main/misc/Blueprint.png)

<!-- Contributors -->
## Contributors
- Lucas Lageweg
- Maximilian Mayer
- Jeren Olsen

# Web Application

# Docker Components

# Kubernetes Components

# Helm

# Execution

# Setup
Before you can start, you need to install the Python requirements listed in `requirements.txt` using the command `pip install -r requirements.txt`.

# Execution
First, start the postgres database, which runs in a Docker container. This is done through `docker compose`, and the coresponding configuration file is part of this directory. So you can just run `docker compose up`. If you want to reset the content in the database, execute `flask --app ./manage.py recreate-database` while the Docker container is running. The volume used for the database is persistant and will remain intact inbetween database runs.

The API is currently not containerized, so you need to just run it on the command line. It will connect to the database via localhost. You can run the API by calling `flask --app ./manage.py --debug run` or by directly executing the `manage.py` file.

You can test the API in a browser such as Firefox. However, you will only receive JSON responses. A proper interface is still missing.

# Scaling and Updating

