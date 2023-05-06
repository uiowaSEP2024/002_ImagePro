import json

import aws_cdk as cdk
import aws_cdk.aws_amplify_alpha as aws_amplify
import aws_cdk.aws_apigateway as aws_apigateway
import aws_cdk.aws_codebuild as aws_codebuild
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.custom_resources as aws_custom_resources
from models import BuildConfig

TRACKER_PREFIX = "TrackerCDK"
AMPLIFY_BRANCH_NAME = "main"


class CdkInfraStack(cdk.Stack):
    def __init__(
        self,
        scope: cdk.App,
        construct_id: str,
        build_config: BuildConfig = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Lambda Function
        function_name = TRACKER_PREFIX + "Function" + "-" + build_config.AppEnv
        cdk_function_name = (
            TRACKER_PREFIX + "Function" + build_config.AppEnv.capitalize()
        )

        tracker_lambda = aws_lambda.Function(
            self,
            cdk_function_name,
            function_name=function_name,
            handler=aws_lambda.Handler.FROM_IMAGE,
            runtime=aws_lambda.Runtime.FROM_IMAGE,
            code=aws_lambda.Code.from_asset_image(directory="../backend"),
            timeout=cdk.Duration.seconds(15),
            environment={
                "APP_ENV": build_config.AppEnv,
                "ALGORITHM": build_config.JwtAlgorithm,
                "ALLOW_ORIGINS": "",
                "SECRET_KEY": cdk.SecretValue.secrets_manager(
                    build_config.SecretKeySecretName,
                ).unsafe_unwrap(),
                "POSTGRES_DB": build_config.DatabaseName
                if build_config.DatabaseName
                else cdk.SecretValue.secrets_manager(
                    build_config.DatabaseAccessSecretName, json_field="dbname"
                ).unsafe_unwrap(),
                "POSTGRES_USER": cdk.SecretValue.secrets_manager(
                    build_config.DatabaseAccessSecretName, json_field="username"
                ).unsafe_unwrap(),
                "POSTGRES_PORT": cdk.SecretValue.secrets_manager(
                    build_config.DatabaseAccessSecretName, json_field="port"
                ).unsafe_unwrap(),
                "POSTGRES_SERVER": cdk.SecretValue.secrets_manager(
                    build_config.DatabaseAccessSecretName, json_field="host"
                ).unsafe_unwrap(),
                "POSTGRES_PASSWORD": cdk.SecretValue.secrets_manager(
                    build_config.DatabaseAccessSecretName, json_field="password"
                ).unsafe_unwrap(),
            },
        )

        # API Gateway Rest API
        tracker_rest_api_deployment_stage = aws_apigateway.StageOptions(
            stage_name=build_config.ApiGatewayStage
        )

        rest_api_name = TRACKER_PREFIX + "RestApi" + "-" + build_config.AppEnv
        cdk_rest_api_name = (
            TRACKER_PREFIX + "RestApi" + build_config.AppEnv.capitalize()
        )

        tracker_rest_api = aws_apigateway.LambdaRestApi(
            self,
            cdk_rest_api_name,
            rest_api_name=rest_api_name,
            handler=tracker_lambda,
            proxy=True,
            deploy_options=tracker_rest_api_deployment_stage,
        )

        # Amplify App
        amplify_app_name = TRACKER_PREFIX + "Amplify" + "-" + build_config.AppEnv
        cdk_amplify_app_id = (
            TRACKER_PREFIX + "Amplify" + build_config.AppEnv.capitalize()
        )

        tracker_amplify_app = aws_amplify.App(
            self,
            cdk_amplify_app_id,
            app_name=amplify_app_name,
            source_code_provider=aws_amplify.GitHubSourceCodeProvider(
                owner=build_config.RepositoryOwner,
                oauth_token=cdk.SecretValue.secrets_manager(
                    build_config.GitHubAccessTokenSecretName
                ),
                repository=build_config.RepositoryName,
            ),
            environment_variables=dict(
                NEXT_PUBLIC_BACKEND_URL=tracker_rest_api.url,
                AMPLIFY_MONOREPO_APP_ROOT=build_config.AmplifyMonoRepoAppRoot,
                AMPLIFY_DIFF_DEPLOY="false",
            ),
            build_spec=aws_codebuild.BuildSpec.from_object_to_yaml(
                {
                    "version": 1,
                    "applications": [
                        {
                            "frontend": {
                                "phases": {
                                    "preBuild": {
                                        "commands": ["npm ci"],
                                    },
                                    "build": {"commands": ["npm run build"]},
                                },
                                "artifacts": {
                                    "baseDirectory": ".next",
                                    "files": ["**/*"],
                                },
                                "cache": {"paths": ["node_modules/**/*"]},
                            },
                            "appRoot": build_config.AmplifyMonoRepoAppRoot,
                        }
                    ],
                }
            ),
        )

        tracker_amplify_app_main_branch = tracker_amplify_app.add_branch(
            amplify_app_name + "-" + AMPLIFY_BRANCH_NAME,
            branch_name=AMPLIFY_BRANCH_NAME,
            stage="PRODUCTION",
            auto_build=True,
        )

        tracker_amplify_app.node.default_child.platform = "WEB_COMPUTE"

        # Amplify App Build Trigger on Create
        build_trigger = aws_custom_resources.AwsCustomResource(
            self,
            TRACKER_PREFIX
            + "AmplifyBuildTrigger"
            + AMPLIFY_BRANCH_NAME.capitalize()
            + build_config.AppEnv.capitalize(),
            function_name=TRACKER_PREFIX
            + "AmplifyBuildTrigger"
            + "-"
            + AMPLIFY_BRANCH_NAME
            + "-"
            + build_config.AppEnv,
            policy=aws_custom_resources.AwsCustomResourcePolicy.from_sdk_calls(
                resources=aws_custom_resources.AwsCustomResourcePolicy.ANY_RESOURCE
            ),
            on_create=aws_custom_resources.AwsSdkCall(
                service="Amplify",
                action="startJob",
                physical_resource_id=aws_custom_resources.PhysicalResourceId.of(
                    "app-build-trigger"
                ),
                parameters={
                    "appId": tracker_amplify_app.app_id,
                    "branchName": AMPLIFY_BRANCH_NAME,
                    "jobType": "RELEASE",
                    "jobReason": "Auto Start build",
                },
            ),
        )
        cdk.CfnOutput(
            self,
            amplify_app_name + "Domain",
            value="https://"
            + tracker_amplify_app_main_branch.branch_name
            + "."
            + tracker_amplify_app.default_domain,
        )
