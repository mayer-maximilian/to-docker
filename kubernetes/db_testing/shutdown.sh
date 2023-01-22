#! /bin/sh

microk8s kubectl delete deployment postgres
microk8s kubectl delete pvc postgres-pv-claim
microk8s kubectl delete pv postgres-pv-volume
microk8s kubectl delete cm postgres-config
