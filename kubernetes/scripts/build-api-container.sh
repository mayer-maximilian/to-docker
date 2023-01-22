#! /bin/sh

cd ~/Documents/Projects/to-docker/backend/
sudo docker build --build-arg api_port=5008 -t todo-api-image:v1 .
sudo docker tag todo-api-image:v1 lucassctestregistry.azurecr.io/todo-api-image:v1
sudo docker push lucassctestregistry.azurecr.io/todo-api-image:v1