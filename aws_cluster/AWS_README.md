

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
