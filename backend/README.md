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

The next steps in the deployment process involve deploying a Lambda Function and an API Gateway. These steps
can be achieved manually by following AWS documentation and videos on these sites respectively:
1. Creating and Deploying a Lambda Function: https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-images.html
2. Creating and Deploying an API Gateway: https://www.youtube.com/watch?time_continue=876&v=6fE31084Uks&embeds_euri=https%3A%2F%2Fwww.deadbear.io%2Fsimple-serverless-fastapi-with-aws-lambda%2F&source_ve_path=MTM5MTE3LDEzOTExNywxMzkxMTcsMTM5MTE3LDEzOTExNywxMzkxMTcsMTM5MTE3LDEzOTExNywxMzkxMTcsMTM5MTE3LDEzOTExNywxMzkxMTcsMTM5MTE3LDIzODUx&feature=emb_title
