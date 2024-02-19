
# Welcome to CDK Infra project!

This is a Python project generated using AWS CDK (Cloud Development Kit) CLI, using this [tutorial](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html)

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.


## Getting Started
1. To get started with this project you will create a virtualenv for Python to store the application's dependencies.

    To manually create a virtualenv on MacOS and Linux:

    ```shell
    $ python3 -m venv .venv
    ```

2. After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

    ```shell
    $ source .venv/bin/activate
    ```

    If you are a Windows platform, you would activate the virtualenv like this:

    ```shell
    % .venv\Scripts\activate.bat
    ```

3. Once the virtualenv is activated, you can install the required dependencies.
    ```shell
    $ pip install -r requirements.txt
    ```

## Deploying with CDK
At this point you can now use the CDK to prepare the CDK application for deployment.

The CDK application has been configured to run in multiple application environments
e.g `development`, and `production`. Thus, for each command we will specify the desired environment by adding an `app_env` property to the CDK application's context with `-c app_env=<environment>` command arguments.

## Prerequisites
There are some prerequisites required for using CDK scripts. These include:
1. Created an AWS account
2. Created Access Tokens either for the Root or IAM User
3. Downloaded the AWS CLI, and configured an AWS profile with access tokens

   > NB: If you use a non-root IAM User, you will need to assign specific/granular policies such as the following:
   >
   > "AdministratorAccess-Amplify", "AmazonAPIGatewayAdministrator", "AmazonEC2ContainerRegistryFullAccess", "AmazonS3FullAccess", "AmazonSSMFullAccess", "AWSCloudFormationFullAccess", "AWSLambda_FullAccess", "IAMFullAccess"
   >
   > You may narrow down some of these permissions for more security, but this combination of permissions have been tested and work for the purposes of deploying this CDK.

4. Secrets stored in AWS Secrets Manager
   1. `AMPLIFY_GITHUB_ACCESS_TOKEN`: The Next.js Amplify App deployed by this project requires a GitHub access token.
       This token must be set inside of AWS SSM with a name corresponding to `GitHubAccessTokenSecretName` in `cdk.json`
       See [this article](https://aws.amazon.com/blogs/mobile/deploy-a-nextjs-13-application-to-amplify-with-the-aws-cdk/) for detailed steps on the permissions required for the token
   2. `DB_ACCESS_[DEV|PROD|TEST]`: The credentials for accessing the RDS database instance. These correspond with the `DatabaseAccessSecretName` in `cdk.json`. The steps for creating this secret inside of AWS console are
        "AWS Secrets Manager" -> "Store new secret" -> "Credentials for Amazon RDS database" -> "Enter user for database (likely `'postgres'`)" -> "Enter password used in creating the database" -> "Select RDS database instance from list" -> Next -> "Enter secret name. One of `'DB_ACCESS_[DEV|PROD|TEST]'`" -> Finish
   3. `SECRET_KEY_[DEV|PROD|TEST]`: This is the secret that would be used to create JWT access tokens for users once they sign up. Similarly to above,
         you would create a plain-text secret in AWS Secrets Manager as follows:
         "AWS Secrets Manager" -> "Store new secret" -> "Other type of secret" -> "Plain Text" -> "Paste a **SECURE** secret token" -> Next -> "Enter a secret name. One of `'SECRET_KEY_[DEV|PROD|TEST]'`" -> Finish

   > NB: These AWS Secret Manager secrets here are ONLY used at the deployment stage. What happens is that their values are copied over from AWS Secretes Manager into the Environment Variables of the AWS Lambda Function. To change the actual runtime values of the environment variables
   > you will have to change the Environment Variables from the Lambda Console. See the documentation [from AWS](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-config) or in `docs` of this repository for images of the process.
   > The backend application may be improved to dynamically load secrets from AWS Secrets Manager (replicated within the same region as the Lambda for low latency), but this has not been set up at the moment.

## Instructions
The first step of the process is to "synthesize" the CloudFormation (CFN) template for this app. This template specifies the resources to be created by AWS CloudFormation based on the different stacks defined in the CDK application code.

To synthesize the CFN template for this code, run
```shell
$ cdk synth -c app_env=<environment>
```

Once the application is synthesized, you can view the resulting CloudFormation template inside
of `cdk.out` folder.

The final step after synthesis is to deploy the stack and create all associated resources (e.g Lambdas, RestAPI Gateway etc.)
```shell
$ cdk deploy -c app_env=<environment>
```

## Deployed Resources
This CDK project deploys the following resources:
1. Dockerized `backend` application Image to AWS ECR
2. AWS Lambda Function that executes Dockerized Image above
3. AWS (REST) API Gateway that triggers the Lambda Function
4. AWS Amplify Application that builds and runs the `frontend`

## Useful CDK deployment commands

 * `cdk ls -c app_env=<environment>`          List all stacks in the app
 * `cdk synth -c app_env=<environment>`       Emits the synthesized CloudFormation template
 * `cdk deploy -c app_env=<environment>`      Deploy this stack to your default AWS account/region
 * `cdk diff -c app_env=<environment>`        Compare deployed stack with current state


# Using Alternate AWS Profiles
To perform any of the above actions using a different AWS account/region, simply setup a new profile with the AWS CLI using the following command:

```bash
aws configure --profile <my-other-profile>
```
Follow the prompts to set up the new profile.

Now, you can run any of the commands above with the `--profile=<my-other-profile>` option to use the credentials and configuration for that AWS profile.

 * `cdk docs`        open CDK documentation

Enjoy!
