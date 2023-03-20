import os

import aws_cdk as cdk
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_apigateway as aws_apigateway
import aws_cdk.aws_ecr as aws_ecr

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

        function_name = "Team8CDKFunction" + "-" + build_config.AppEnv
        cdk_function_name = "Team8CDKFunction" + build_config.AppEnv.capitalize()

        team8_lambda = aws_lambda.Function(
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
            },
        )

        team8_rest_api_deployment_stage = aws_apigateway.StageOptions(
            stage_name=build_config.ApiGatewayStage
        )

        team8_rest_api = aws_apigateway.LambdaRestApi(
            self,
            "Team8CDKRestApi",
            rest_api_name="Team8CDKRestApi",
            handler=team8_lambda,
            proxy=True,
            deploy_options=team8_rest_api_deployment_stage,
        )
