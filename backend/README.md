# backend
This is the backend project for Team03's SEP project.


# Get Started

Before starting the application, make sure to start a Virtual Environment for your project by using the command:

```bash
source venv/bin/activate
```

Once the Venv is fired up, make sure to install all requirements required for the project:

```bash
pip install -r requirements.txt
```

To start the application, run:

```bash
bash run-dev.sh
```

OR

```bash
uvicorn app.main:app --reload
```


# Running Migrations
Here are some scripts for working with migrations:

**Autogenerate a new migration**
```bash
alembic revision --autogenerate -m "<migration_name>"
```

**Apply all migrations**
```bash
alembic upgrade head
```

**Reset all migrations**

```bash
alembic downgrade base
```

**Reset last migration**
```bash
alembic downgrade -1
```

# Run Tests
To execute tests, run:

(With test coverage)
```bash
bash run-test.sh
```

OR

```bash
pytest
```

# Deployment (⚠️ In Progress)
The backend for this project can be deployed to AWS Lambda service with the
following step:

1. Build the docker image
    ```bash
   docker build --build-arg APP_ENV=production -t team8-backend .    
   ```
2. Authenticate local docker CLI to AWS Elastic Container Registry
    ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com
    ```
3. Create a repository on AWS ECR
    ```bash
   aws ecr create-repository --repository-name team8backend --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
    ```
4. Tag the locally created image (from step 1), to match the ECR repository name
    ```bash
   docker tag  team8-backend:latest <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/team8-backend:latest
    ```
5. Push the tagged container to the ECR repository
    ```bash
   docker push <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/team8-backend:latest
   ```



Once the docker image has been deployed to AWS Lambda, we need to also set up an AWS API Gateway
trigger for the Lambda function. To do so, we use the following commands. [source](https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-awscli.html):

1. Go to the AWS ECR dashboard and identify the container you have just deployed. It should have a 'latest' tag
2. Copy the URI of the image
3. Create a role for the lambda function we will be deploying (if it does not exist already)
   ```bash
   aws iam create-role --role-name lambda-ex \
   --assume-role-policy-document '{"Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]}'
   ```
4. Attach permissions to the created role, to allow the function to write logs to CloudWatch (if it does not exist already)
   ```bash
   aws iam attach-role-policy --role-name lambda-ex --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
   ```
5. Create the lambda function (if it does not exist already)
   ```bash
   aws lambda create-function --region sa-east-1 --function-name Team8Function \
    --package-type Image  \
    --code ImageUri=<aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/team8-backend:latest   \
    --role arn:aws:iam::<aws-account-id>:role/lambda-ex 
   ```
   
Once your function is created, you will need to create an API Gateway that will trigger the lambda when it receives a
request over the browser. For doing so follow the following commands:

1. Create the RESt API (if it does not exist yet)
   ```bash
   aws apigateway create-rest-api --name 'Team8RestApi' --description 'The Team 8 REST API'
   ```
2. Get the ID of the newly created rest-api
   ```bash
   aws apigateway get-rest-apis --query '(items[?name==`Team8RestApi`].id)[0]'
   ```
   
3. Get the root resource id
   ```bash
   aws apigateway get-resources --rest-api-id <the-rest-api-id> --query '(items[?path==`/`])[0].id'
   ```
   
4. Create an ANY HTTP Method on the REST API (if it does not exist yet)
   ```bash
   aws apigateway put-method --rest-api-id <the-rest-api-id> \
     --resource-id <the-root-resource-id> \
     --http-method ANY \
     --authorization-type "NONE" \
     --no-api-key-required 
   ```

5. Create the Lambda Integration on the API Gateway (if it does not exist yet)
   ```bash
   aws apigateway put-integration --rest-api-id <the-rest-api-id> \
   --resource-id <the-resource-id> --http-method ANY --type AWS \
   --integration-http-method POST \
   --uri 'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:<the-aws-account-id>:function:<the-lambda-function-name>/invocations'
   ```

6. Create the method response for the ANY method on the root resource
   ```bash
   aws apigateway put-method-response --rest-api-id <the-rest-api-id> \
     --resource-id <the-root-resource-id> --http-method ANY \
     --status-code 200 \
     --response-models "application/json=Empty"
   ```
   
// TODO: create stage and then create deployment at the end of the entire process
