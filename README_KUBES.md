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

7. Build Backend Image in Minikube

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
kubectl apply -f postgres_kube_persistantvolume_statefullset.yaml
kubectl apply -f postgres_kube_persistantvolumeclaim.yaml
kubectl apply -f postgres_kube_secret.yaml
```
