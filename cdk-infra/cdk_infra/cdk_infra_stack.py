import os

import aws_cdk as cdk
import aws_cdk.aws_lambda as aws_lambda
import aws_cdk.aws_apigateway as aws_apigateway
import aws_cdk.aws_ecr as aws_ecr


class CdkInfraStack(cdk.Stack):
    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        team8_ecr_repository = aws_ecr.Repository.from_repository_name(self, 'Team8CDKRepository', 'team8-backend')
        team8_lambda = aws_lambda.Function(
            self,
            "Team8CDKFunction",
            handler=aws_lambda.Handler.FROM_IMAGE,
            runtime=aws_lambda.Runtime.FROM_IMAGE,
            code=aws_lambda.Code.from_ecr_image(
               team8_ecr_repository, tag="latest",
            ),
            function_name="Team8CDKFunction",
        )

        team8_rest_api = aws_apigateway.LambdaRestApi(
            self,
            "Team8CDKRestApi",
            handler=team8_lambda,
            proxy=True,
            rest_api_name="Team8CDKApi"
        )


