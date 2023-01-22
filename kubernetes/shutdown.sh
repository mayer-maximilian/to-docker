#! /bin/sh

microk8s kubectl delete ingress todo-ingress
microk8s kubectl delete deployment todo-frontend-deployment

microk8s kubectl delete deployment todo-api-deployment
microk8s kubectl delete deployment todo-redis-deployment
microk8s kubectl delete deployment todo-database-deployment

microk8s kubectl delete pvc todo-database-pvc
microk8s kubectl delete pv todo-database-data

microk8s kubectl delete cm todo-database-config
microk8s kubectl delete secret todo-database-secret

microk8s kubectl delete service todo-frontend-service
microk8s kubectl delete service todo-api-service
microk8s kubectl delete service todo-redis-service
microk8s kubectl delete service todo-database-service