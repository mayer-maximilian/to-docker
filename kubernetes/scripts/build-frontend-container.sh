#! /bin/sh

cd ~/Documents/Projects/to-docker/frontend/
sudo docker build --build-arg api_port=5008 -t todo-frontend-image:v1 .
sudo docker tag todo-frontend-image:v1 lucassctestregistry.azurecr.io/todo-frontend-image:v1
sudo docker push lucassctestregistry.azurecr.io/todo-frontend-image:v1