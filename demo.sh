# build and push api container
cd backend
sudo docker build --build-arg api_port=5008 --build-arg redis_port=6379 --build-arg api_env=develop -t lucassctestregistry.azurecr.io/todo-api-image:v1 -t lucassctestregistry.azurecr.io/todo-api-image:latest .
sudo docker push lucassctestregistry.azurecr.io/todo-api-image --all-tags

# build and push frontend container
cd ../frontend
sudo docker build --build-arg api_port=5008 -t lucassctestregistry.azurecr.io/todo-frontend-image:v1 -t lucassctestregistry.azurecr.io/todo-frontend-image:latest .
sudo docker push lucassctestregistry.azurecr.io/todo-frontend-image --all-tags

# demonstrate empty cluster
kubectl get all -n todo-app

# install ClusterIssuer
cd ../kubernetes
kubectl apply -f ./networking/cluster-issuer.yml

# install using helm
cd  ../todo-app-helm/todo-app
helm dependency update
cd ..
helm install todo-app todo-app --namespace=todo-app --create-namespace
helm list -n todo-app
kubectl get all -n todo-app

# NOTE: DEMONSTRATE APP

# scaling frontend
kubectl get pods -n todo-app
kubectl scale deployment frontend-deployment --replicas=10 -n todo-app
kubectl get pods -n todo-app
kubectl scale deployment api-deployment --replicas=3 -n todo-app
kubectl get pods -n todo-app

# NOTE: UPDATE SOURCE CODE

# update frontend container
cd ../frontend
sudo docker build --build-arg api_port=5008 -t lucassctestregistry.azurecr.io/todo-frontend-image:v2 -t lucassctestregistry.azurecr.io/todo-frontend-image:latest .
sudo docker push lucassctestregistry.azurecr.io/todo-frontend-image --all-tags

# perform rollout
kubectl rollout restart deployment/frontend-deployment -n todo-app

# NOTE: DEMONSTRATE APP

# rollback
kubectl rollout undo deployment/frontend-deployment -n todo-app

# NOTE: DEMONSTRATE APP

# perform canary
cd ../kubernetes
kubectl apply -f ./deployments/frontend-canary-deployment.yml
kubectl scale deployment frontend-canary-deployment --replicas=5 -n todo-app
kubectl scale deployment frontend-deployment --replicas=5 -n todo-app
kubectl get pods -n todo-app

# NOTE: DEMONSTRATE APP

# finish canary
kubectl scale deployment frontend-canary-deployment --replicas=10 -n todo-app
kubectl delete deployment frontend-depolyment
kubectl get pods -n todo-app

# uninstall using helm
helm uninstall -n todo-app
helm list -n todo-app