# Starting MiniKube

1. Assuing you have installed MiniKube and Kubectl on your machine, you can start MiniKube by running the following command:

```bash
minikube start
minikube status
minikube dashboard
```


4. Build Frontend Image in Minikube

```bash
eval $(minikube docker-env)
docker build -t 002_imagepro-frontend:latest --file Dockerfile_Frontend .
```

5. Create a Deployment for Frontend

```bash
kubectl apply -f frontend_kube_deployment.yaml
kubectl apply -f frontend_kube_service.yaml
```

6. Add ingress to minikube and verify the nginx controller is running
```bash
minikube addons enable ingress
kubectl get pods -n ingress-nginx
```
7. Verify the frontend service is running
```bash
minikube service frontend-service --url
```

9. Build Backend Image in Minikube

```bash
eval $(minikube docker-env)
docker build -t 002_imagepro-backend:latest --file Dockerfile_Backend .
```

8. Create a Deployment for Backend

```bash
kubectl apply -f backend_kube_deployment.yaml
kubectl apply -f backend_kube_service.yaml
```

9. Create A Volume for Persistent Storage

```bash
kubectl apply -f postgres_kube_persistantvolume.yaml
kubectl apply -f postgres_kube_persistantvolume_service.yaml
kubectl apply -f postgres_kube_persistantvolume_statefulset.yaml
kubectl apply -f postgres_kube_persistantvolumeclaim.yaml
kubectl apply -f postgres_kube_secrets.yaml
```
10. To restart all pods and services
```bash
kubectl delete all --all -n default
```

11. Testing Frontend and Backend Connection

To ensure that the frontend and backend pods are connected, you can go to minikube dashboard and enter the
frontend pod and run the following command in the exec shell:

```bash
curl -X POST "http://backend-service/login" \
     -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
     --data-urlencode "username=admin1@admin.com" \
     --data-urlencode "password=abcdefg" \
     --cookie-jar cookie.txt \
     --cookie cookie.txt \
     --include
```
You should get a response with a 200 status code and an access token in it for a successful login
If you go to the logs of the backend pod, you should see a successful POST /login request
