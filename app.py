#!/usr/bin/env python3
import os

import aws_cdk as cdk

from pipeline_new.pipeline_new_stack import AwsCodepipelineStack


app = cdk.App()
AwsCodepipelineStack(app, "PipelineStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    env=cdk.Environment(account='940394231405', region='ap-south-1'),
    stack_name='github-codepipeline-stack'

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
