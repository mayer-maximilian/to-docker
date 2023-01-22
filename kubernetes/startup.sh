#! /bin/sh

# ./scripts/build-api-container.sh

# setup services for different pods to commuunicate with each other (we use service names, so this requires a DNS)
microk8s kubectl apply -f ./services.yml

# setup database, including the required persistant storage
microk8s kubectl apply -f ./database-storage.yml
microk8s kubectl apply -f ./database-config.yml
microk8s kubectl apply -f ./database-deployment.yml

# setup api + components
microk8s kubectl apply -f ./redis-deployment.yml
microk8s kubectl apply -f ./api-deployment.yml

# setup frontend and ingress
microk8s kubectl apply -f ./frontend-deployment.yml
microk8s kubectl apply -f ./ingress.yml

# microk8s kubectl get pods