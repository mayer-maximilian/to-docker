#! /bin/sh
microk8s kubectl apply -f ./database-config.yml
microk8s kubectl apply -f ./database-storage.yml
microk8s kubectl apply -f ./database-deployment.yml
microk8s kubectl apply -f ./redis-deployment.yml
microk8s kubectl apply -f ./api-deployment.yml
#microk8s kubectl apply -f ./frontend-deployment.yml
#microk8s kubectl apply -f ./services.yml
#microk8s kubectl apply -f ./ingress.yml