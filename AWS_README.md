

- CREATING AN ACCESS ENTRY TO THE EKS CLUSTER FOR YOUR IAM USER ACCOUNT
```bash
aws eks create-access-entry --cluster-name THE-CLUSTER-NAME --principal-arn arn:aws:iam::YOUR-ID-NUMBER:user/YOUR-USERNAME
\  --type STANDARD --username YOUR-USERNAME
```
This can also be done through the GUI if you access our cluster through the EKS portal and go to the Access tab.
Then you can create an access entry for your IAM user account, and add an access policy
("AmazonEKSClusterAdminPolicy" gives you permissions for all actions on all resources)
