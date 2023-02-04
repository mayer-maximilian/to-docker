#! /bin/sh

microk8s kubectl delete -f ../networking/ingress.yml

microk8s kubectl delete -f ../deployments/frontend-deployment.yml
microk8s kubectl delete -f ../deployments/api-deployment.yml
microk8s kubectl delete -f ../deployments/redis-deployment.yml
microk8s kubectl delete -f ../deployments/database-deployment.yml

#microk8s kubectl delete -f ../access-control/operator.yml
#microk8s kubectl delete -f ../access-control/developer.yml
#microk8s kubectl delete -f ../access-control/admin.yml

# microk8s kubectl delete -f ../networking/cluster-issuer.yml
#microk8s kubectl delete -f ../networking/network-policies.yml

microk8s kubectl delete -f ../config/config.yml
microk8s kubectl delete -f ../config/namespace.yml