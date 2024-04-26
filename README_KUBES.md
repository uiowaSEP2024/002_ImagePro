# Starting MiniKube

1. Assuming you have installed MiniKube and Kubectl on your machine, you can start MiniKube by running the following command:

    ```bash
    minikube start
    minikube status
    minikube dashboard
    ```

2. Build Frontend Image in Minikube

    ```bash
    eval $(minikube docker-env)
    docker build -t 002_imagepro-frontend:latest --file Dockerfile_Frontend .
    ```

3. Create a Deployment for Frontend

    ```bash
    kubectl apply -f frontend_kube_deployment.yaml
    kubectl apply -f frontend_kube_service.yaml
    ```

4. Add ingress to Minikube and verify the nginx controller is running

    ```bash
    minikube addons enable ingress
    kubectl get pods -n ingress-nginx
    ```

5. Verify the frontend service is running

    ```bash
    minikube service frontend-service --url
    ```

6. Build Backend Image in Minikube

    ```bash
    eval $(minikube docker-env)
    docker build -t 002_imagepro-backend:latest --file Dockerfile_Backend .
    ```

7. Create a Deployment for Backend

    ```bash
    kubectl apply -f backend_kube_deployment.yaml
    kubectl apply -f backend_kube_service.yaml
    ```

8. Create A Volume for Persistent Storage

    ```bash
    kubectl apply -f postgres_kube_persistantvolume.yaml
    kubectl apply -f postgres_kube_persistantvolume_service.yaml
    kubectl apply -f postgres_kube_persistantvolume_statefulset.yaml
    kubectl apply -f postgres_kube_persistantvolumeclaim.yaml
    kubectl apply -f postgres_kube_secrets.yaml
    ```

9. Create a deployment/services/ingress for the internal server

    ```bash
    docker build -t orthanc-for-kube:latest --file Dockerfile_OrthancKube .
    kubectl apply -f orthanc_kube_deployment.yaml
    kubectl apply -f orthanc_kube_service.yaml
    kubectl apply -f orthanc_send_dicom_service.yaml
    kubectl apply -f orthanc_ingress.yaml
    ```

10. Build the study image for the study kube job

    ```bash
    docker build -t study:latest --file Dockerfile_Study .
    ```

11. Create the image/deployment for the study kube job

    ```bash
    docker build -t receiver_loop:latest --file Dockerfile_ReceiverLoop .
    kubectl apply -f receiver_deployment.yaml
    ```

12. Create the service account

    ```bash
    kubectl apply -f role.yaml
    kubectl apply -f role_binding.yaml
    kubectl apply -f service_account.yaml
    ```

13. If you are on MacOS, add the following to /etc/hosts

    ```bash
    127.0.0.1 internal-orthanc.com
    ```

14. To send data from a hospital to the internal server, run the tmux_startup script but ONLY run the hospital. Then open up a new terminal and set up port forwarding to the internal server

    ```bash
    kubectl port-forward service/orthanc-send-dicom-service 4026:4026
    ```

    Open up another new terminal and run

    ```bash
    minikube tunnel
    ```

    Once those are running, you should be able to navigate to `internal-orthanc.com` and `localhost:8030` and send DICOM data like normal. Then you can send data to the internal server by running the following command

15. To restart all pods and services

    ```bash
    kubectl delete all --all -n default
    ```

16. Testing Frontend and Backend Connection

    To ensure that the frontend and backend pods are connected, you can go to Minikube dashboard and enter the frontend pod and run the following command in the exec shell:

    ```bash
    curl -X POST "http://backend-service/login" \
         -H "Content-Type: application/x-www-form-urlencoded;charset=UTF-8" \
         --data-urlencode "username=admin1@admin.com" \
         --data-urlencode "password=abcdefg" \
         --cookie-jar cookie.txt \
         --cookie cookie.txt \
         --include
    ```

    You should get a response with a 200 status code and an access token in it for a successful login. If you go to the logs of the backend pod, you should see a successful POST /login request.
