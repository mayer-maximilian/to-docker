#! /bin/sh

cd ~/Documents/Projects/to-docker/backend/
sudo docker build --build-arg api_port=5008 --build-arg api_env=develop --build-arg redis_host=redis-service --build-arg redis_port=6379 -t todo-api-image:v1 .
sudo docker tag todo-api-image:v1 lucassctestregistry.azurecr.io/todo-api-image:v1
sudo docker push lucassctestregistry.azurecr.io/todo-api-image:v1