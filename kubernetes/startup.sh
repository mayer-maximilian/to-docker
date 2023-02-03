#! /bin/sh

microk8s kubectl apply -f ./config/namespace.yml
microk8s kubectl apply -f ./config/config.yml

#microk8s kubectl apply -f ./access-control/admin-role.yml
#microk8s kubectl apply -f ./access-control/developer-role.yml
#microk8s kubectl apply -f ./access-control/operator-role.yml

microk8s kubectl apply -f ./deployments/database-deployment.yml
microk8s kubectl apply -f ./deployments/redis-deployment.yml
microk8s kubectl apply -f ./deployments/api-deployment.yml
microk8s kubectl apply -f ./deployments/frontend-deployment.yml

#microk8s kubectl apply -f ./networking/network-policies.yml
microk8s kubectl apply -f ./networking/cluster-issuer.yml
microk8s kubectl apply -f ./networking/ingress.yml