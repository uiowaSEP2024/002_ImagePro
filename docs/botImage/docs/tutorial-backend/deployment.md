---
sidebar_position: 4
---

# Deployment

These are instructions to deploy the backend. The backend is deployed to AWS Lambda with AWS API Gateway, and uses AWS RDS for the database.

## Introduction
The backend is deployed using the AWS Cloud Development Kit (CDK). The CDK is an open-source software development framework to define cloud infrastructure in code and provision it through AWS CloudFormation.


## Prerequisites

1. [Create an AWS Account](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-creating.html)
2. [Create an AWS IAM User](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) and [Assign an Access Key](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)
3. [Install](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) and [Configure](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html) AWS CLI
4. [Install](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_install) and [Bootstrap](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html#getting_started_bootstrap) the AWS CDK


## Deployment Setup
For this project, all the logic for managing deployment with CDK is in the `cdk-infra` directory. From inside this directory, we can run the commands in the next section to create the CloudFormation templates describing the resources we want to deploy, and then deploy them to AWS.

## Process
1. Synthesize the CloudFormation template for the desired environment
    ```bash
    cdk synth -c app_env=<environment>
    ```
2. Check differences between the synthesized template and the deployed stack
    ```bash
    cdk diff -c app_env=<environment>
    ```
3. Deploy the CloudFormation template for the desired environment
    ```bash
    cdk deploy -c app_env=<environment>
    ```


