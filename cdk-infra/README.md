
# Welcome to CDK Infra project!

This is a Python project generated using AWS CDK (Cloud Development Kit) CLI, using this [tutorial](https://docs.aws.amazon.com/cdk/v2/guide/hello_world.html)

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project. 


## Getting Started
To get started with this project you will create a virtualenv for Python to store the application's dependencies.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

## Deploying with CDK
At this point you can now use the CDK to prepare the CDK application for deployment. 

The CDK application has been configured to run in multiple application environments e.g `development`, and `production`. Thus, for each command we will specify the desired environment by adding an `app_env` property to the CDK application's context with `-c app_env=<environment>` command arguments.

The first step of the process is to "synthesize" the CloudFormation (CFN) template for this app. This template specifies the resources to be created by AWS CloudFormation based on the different stacks defined in the CDK application code.

To synthesize the CFN template for this code, run
```
$ cdk synth -c app_env=<environment>
```

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
Follow the prompts to setup the new profile.

Now, you can run any of the commands above with the `--profile=<my-other-profile>` option to use the credentials and configuration for that AWS profile.
 
 * `cdk docs`        open CDK documentation

Enjoy!
