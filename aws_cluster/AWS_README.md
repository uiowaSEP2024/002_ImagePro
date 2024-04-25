

- CREATING AN ACCESS ENTRY TO THE EKS CLUSTER FOR YOUR IAM USER ACCOUNT
```bash
aws eks create-access-entry --cluster-name THE-CLUSTER-NAME --principal-arn arn:aws:iam::YOUR-ID-NUMBER:user/YOUR-USERNAME
\  --type STANDARD --username YOUR-USERNAME
```
This can also be done through the GUI if you access our cluster through the EKS portal and go to the Access tab.
Then you can create an access entry for your IAM user account, and add an access policy
("AmazonEKSClusterAdminPolicy" gives you permissions for all actions on all resources)

-- Ensure that you have the necessary permissions to create an access entry for your IAM user account. Easiest way is throught the GUI
Using the Acess tab in the EKS portal, you can create an access entry for your IAM user account, and add an access policy
("AmazonEKSClusterAdminPolicy" gives you permissions for all actions on all resources)

-- Check that you are using the correct context

```bash
kubectl config current-context
```

-- If you are not using the correct context, you can change it by running the following command:

```bash
eksctl utils write-kubeconfig --cluster= THE-CLUSTER-NAME --region= YOUR-REGION
```
or
```bash
kubectl config use-context THE-CLUSTER-NAME
```

-- the following command updates your kubeconfig file with the correct context for a new cluster
```bash
aws eks --region <region> update-kubeconfig --name <cluster-name>
```


### Useful Commands

##### Get events sorted by creation time
```bash
kubectl get events --sort-by='.metadata.creationTimestamp'
```
##### Start or Delete all resources in a directory
```bash
kubectl apply --recursive -f <Directory>
kubectl delete --recursive -f <Directory>
```

##### Testing network connectivity between pods
```bash
kubectl run curlpod --image=radial/busyboxplus:curl -i --tty --rm
# Inside the pod
curl frontend-service.default:3000


```
# TODO's/ possible fixes

- [ ] Figure out how to interpret the cloudwatch logs https://us-east-1.console.aws.amazon.com/cloudwatch/

```text
Failures

111s        Warning   Failed                    pod/frontend-86db8dfdfc-xczc5            Error: ImagePullBackOff
6s          Warning   Failed                    pod/frontend-86db8dfdfc-xczc5            Failed to pull image "325852638497.dkr.ecr.us-east-1.amazonaws.com/manual_gui_ecr:frontend_test": failed to pull and unpack image "325852638497.dkr.ecr.us-east-1.amazonaws.com/manual_gui_ecr:frontend_test": failed to resolve reference "325852638497.dkr.ecr.us-east-1.amazonaws.com/manual_gui_ecr:frontend_test": failed to do request: Head "https://325852638497.dkr.ecr.us-east-1.amazonaws.com/v2/manual_gui_ecr/manifests/frontend_test": dial tcp 10.0.2.110:443: i/o timeout
```
- [ ] Find a way to link the EKS cluster/ Image pull to the ECR container registry
- [ ] Create a DockerHub account and link the EKS cluster to the DockerHub container registry
- [ ] Ensure that we are using the correct ARN for the ECR container registry
- [ ] Configure secrets for the ECR container registry that we are using
- [ ] Ensure that we have all correct permissions
  - https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_EKS.html
  - https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html

```text
3m23s       Warning   InvalidDiskCapacity       node/fargate-ip-10-0-2-55.ec2.internal   invalid capacity 0 on image filesystem

```


- [ ] Find a way to increase the disk capacity on the image filesystem for the fargate node
  - Usure if this is a problem or not, but it is something to look into
  - This could be a problem with the fargate node, and not the EKS cluster itself
  - Could be that the service is not configured correctly, or that the fargate node is not configured correctly





- Building frontend image in amd64 (it was arm64 naturally, but aws nodes use amd64 OS environment, this makes our image compatible work on the proper aws OS)
```bash
docker buildx build --platform linux/amd64 -t 325852638497.dkr.ecr.us-east-1.amazonaws.com/manual_gui_ecr:frontend_test --file Dockerfile_frontend_aws --push .
```

- Link for setting up an ALB ingress controller for our cluster: https://aws.amazon.com/blogs/containers/using-alb-ingress-controller-with-amazon-eks-on-fargate/



Trying to create the EFS Set up / 4-23-2024

1. Ran the following commands:

```bash
eksctl utils associate-iam-oidc-provider --region us-east-1 --cluster SEP-Cluster --approve
```
Then

```bash
export cluster_name=SEP-Cluster
export role_name=AmazonEKS_EFS_CSI_DriverRole
eksctl create iamserviceaccount \
    --name efs-csi-controller-sa \
    --namespace kube-system \
    --cluster $cluster_name \
    --role-name $role_name \
    --role-only \
    --attach-policy-arn arn:aws:iam::aws:policy/service-role/AmazonEFSCSIDriverPolicy \
    --approve
TRUST_POLICY=$(aws iam get-role --role-name $role_name --query 'Role.AssumeRolePolicyDocument' | \
    sed -e 's/efs-csi-controller-sa/efs-csi-*/' -e 's/StringEquals/StringLike/')
aws iam update-assume-role-policy --role-name $role_name --policy-document "$TRUST_POLICY"
```
These two commands create an IAM role for EFS driver to interact with EFS file system

2. Install the EFS Driver add-on to our cluster on the AWS Console

3. Go to EFS and create a file system
   - Follow the tutorial listed on the EFS CSI Driver page:
     https://github.com/kubernetes-sigs/aws-efs-csi-driver/blob/master/docs/efs-create-filesystem.md
