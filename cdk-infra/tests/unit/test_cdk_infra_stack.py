import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_infra.cdk_infra_stack import CdkInfraStack
from app import get_config_for_app_env

import json

with open("cdk.json") as fp:
    context = json.load(fp)["context"]


def test_stack_created():
    app = core.App(context=context)

    build_config = get_config_for_app_env(app, app_env="test")

    stack = CdkInfraStack(app, "test-cdk-infra", build_config)
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "FunctionName": "Team3CDKFunction-test",
            "PackageType": "Image",
            "Environment": {"Variables": {"APP_ENV": "test"}},
        },
    )

    template.has_resource("AWS::ApiGateway::RestApi", {})

    template.has_resource_properties("AWS::ApiGateway::Stage", {"StageName": "test"})

    template.has_resource_properties(
        "AWS::Amplify::App", {"Name": "Team3CDKAmplifyApp-test"}
    )
    template.has_resource_properties("AWS::Amplify::Branch", {"BranchName": "main"})
