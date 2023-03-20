#!/usr/bin/env python3
import os

import aws_cdk as cdk

from cdk_infra.cdk_infra_stack import CdkInfraStack

from models import BuildConfig


def get_config_for_app_env(cdk_app: cdk.App, app_env=None):
    app_env: str = app_env if app_env else cdk_app.node.try_get_context("app_env")

    if not app_env:
        raise Exception(
            "Context variable missing on CDK command. Pass in as `-c app_env=development|production`"
        )

    default_config: dict = cdk_app.node.try_get_context("default")
    app_env_config: dict = cdk_app.node.try_get_context(app_env)

    print(default_config, app_env_config)

    return BuildConfig.parse_obj({**default_config, **app_env_config})


def main():
    app = cdk.App()

    build_config = get_config_for_app_env(app)

    cdk.Tags.of(app).add("AppName", build_config.AppName)
    cdk.Tags.of(app).add("AppEnv", build_config.AppEnv)

    stack_name = "-".join([build_config.AppName, build_config.AppEnv])

    CdkInfraStack(app, stack_name, build_config=build_config)

    app.synth()


if __name__ == "__main__":
    main()
