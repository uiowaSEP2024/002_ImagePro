#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_infra.cdk_infra_stack import CdkInfraStack


from models import BuildConfig

app = cdk.App()


def get_config_for_app_env():
    app_env: str = app.node.try_get_context('app_env')

    if not app_env:
        raise Exception("Context variable missing on CDK command. Pass in as `-c app_env=development|production`")

    default_config: dict = app.node.try_get_context('default')
    raw_config: dict = app.node.try_get_context(app_env)

    return BuildConfig.parse_obj({**default_config, **raw_config})


def main():
    build_config = get_config_for_app_env()

    cdk.Tags.of(app).add('AppName', build_config.AppName)
    cdk.Tags.of(app).add('AppEnv', build_config.AppEnv)

    stack_name = '-'.join([build_config.AppName, build_config.AppEnv])

    CdkInfraStack(app, stack_name,
                  build_config=build_config
                  # If you don't specify 'env', this stack will be environment-agnostic.
                  # Account/Region-dependent features and context lookups will not work,
                  # but a single synthesized template can be deployed anywhere.

                  # Uncomment the next line to specialize this stack for the AWS Account
                  # and Region that are implied by the current CLI configuration.

                  # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

                  # Uncomment the next line if you know exactly what Account and Region you
                  # want to deploy the stack to. */

                  # env=cdk.Environment(account='123456789012', region='us-east-1'),

                  # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                  )

    app.synth()


if __name__ == '__main__':
    main()
