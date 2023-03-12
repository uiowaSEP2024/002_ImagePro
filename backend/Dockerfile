FROM public.ecr.aws/lambda/python:3.10

ARG APP_ENV
ENV APP_ENV ${APP_ENV}

RUN yum update -y

# Install amazon-linux-extras
RUN yum install -y amazon-linux-extras

# Enable postgresql14 features to allow auto installing postgresql-devel-14 + libpq v10+
RUN PYTHON=python2 amazon-linux-extras enable postgresql14

# Install postgresql psycopg2 dependencies and python deps
RUN yum install -y gcc python-dev postgresql-devel

# Copy project code
COPY app ${LAMBDA_TASK_ROOT}/app
COPY config ${LAMBDA_TASK_ROOT}/config
COPY alembic ${LAMBDA_TASK_ROOT}/alembic
COPY alembic.ini ${LAMBDA_TASK_ROOT}/alembic.ini
COPY tasks.py ${LAMBDA_TASK_ROOT}/tasks.py
COPY root.py ${LAMBDA_TASK_ROOT}/root.py


# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY requirements.txt  .

RUN  pip3 install -r "${LAMBDA_TASK_ROOT}/requirements.txt"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app/main.handler" ]