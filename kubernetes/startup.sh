#! /bin/sh

# ./scripts/build-api-container.sh

# setup services for different pods to commuunicate with each other (we use service names, so this requires a DNS)
microk8s kubectl apply -f ./services/services.yml

# setup database, including the required persistant storage
microk8s kubectl apply -f ./storage/database-storage.yml
microk8s kubectl apply -f ./config/database-config.yml
microk8s kubectl apply -f ./deployments/database-deployment.yml

# setup api + components
microk8s kubectl apply -f ./deployments/redis-deployment.yml
microk8s kubectl apply -f ./deployments/api-deployment.yml

# setup frontend and ingress
microk8s kubectl apply -f ./deployments/frontend-deployment.yml
microk8s kubectl apply -f ./ingresses/ingress.yml

# microk8s kubectl get pods