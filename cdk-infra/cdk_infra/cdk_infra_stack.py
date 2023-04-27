import json

import aws_cdk as cdk
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_apigateway as aws_apigateway
import aws_cdk.aws_amplify_alpha as aws_amplify
import aws_cdk.aws_codebuild as aws_codebuild
import aws_cdk.custom_resources as aws_custom_resources

from models import BuildConfig


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
        function_name = "Team3CDKFunction" + "-" + build_config.AppEnv
        cdk_function_name = "Team3CDKFunction" + build_config.AppEnv.capitalize()

        team3_lambda = aws_lambda.Function(
            self,
            cdk_function_name,
            function_name=function_name,
            handler=aws_lambda.Handler.FROM_IMAGE,
            runtime=aws_lambda.Runtime.FROM_IMAGE,
            code=aws_lambda.Code.from_asset_image(directory="../backend"),
            timeout=cdk.Duration.seconds(15),
            environment={
                "APP_ENV": build_config.AppEnv,
                "POSTGRES_DB": build_config.PostgresDbName,
                "POSTGRES_USER": build_config.PostgresUser,
                "POSTGRES_PORT": str(build_config.PostgresPort),
                "ALGORITHM": build_config.JwtAlgorithm,
                "ALLOW_ORIGINS": ""
            },
        )

        # API Gateway Rest API
        team3_rest_api_deployment_stage = aws_apigateway.StageOptions(
            stage_name=build_config.ApiGatewayStage
        )

        rest_api_name = "Team3CDKRestApi" + "-" + build_config.AppEnv
        cdk_rest_api_name = "Team3CDKRestApi" + build_config.AppEnv.capitalize()

        team3_rest_api = aws_apigateway.LambdaRestApi(
            self,
            cdk_rest_api_name,
            rest_api_name=rest_api_name,
            handler=team3_lambda,
            proxy=True,
            deploy_options=team3_rest_api_deployment_stage,
        )

        # Amplify App
        amplify_app_name = "Team3CDKAmplifyApp" + "-" + build_config.AppEnv
        cdk_amplify_app_id = "Team3CDKAmplifyApp" + build_config.AppEnv.capitalize()

        team3_amplify_app = aws_amplify.App(
            self,
            cdk_amplify_app_id,
            app_name=amplify_app_name,
            source_code_provider=aws_amplify.GitHubSourceCodeProvider(
                owner=build_config.RepositoryOwner,
                oauth_token=cdk.SecretValue.secrets_manager("TEAM3_GITHUB_TOKEN_KEY"),
                repository=build_config.RepositoryName,
            ),
            environment_variables=dict(
                BACKEND_URL=team3_rest_api.url,
                AMPLIFY_MONOREPO_APP_ROOT="frontend",
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
                            "appRoot": "frontend",
                        }
                    ],
                }
            ),
        )

        branch_name = "main"

        team3_amplify_app.add_branch(
            amplify_app_name + "-" + branch_name,
            branch_name=branch_name,
            stage="PRODUCTION",
            auto_build=True,
        )

        team3_amplify_app.node.default_child.platform = "WEB_COMPUTE"

        # Amplify App Build Trigger on Create
        build_trigger = aws_custom_resources.AwsCustomResource(
            self,
            "Team3CDKTriggerAmplifyAppBuild" + build_config.AppEnv.capitalize(),
            function_name="Team3CDKTriggerAmplifyAppBuild" + "-" + build_config.AppEnv,
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
                    "appId": team3_amplify_app.app_id,
                    "branchName": branch_name,
                    "jobType": "RELEASE",
                    "jobReason": "Auto Start build",
                },
            ),
        )
        cdk.CfnOutput(self, amplify_app_name + "AppId", value=team3_amplify_app.app_id)
        cdk.CfnOutput(self, amplify_app_name + "DefaultDomain", value=team3_amplify_app.default_domain)
