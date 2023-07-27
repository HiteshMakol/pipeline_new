# from aws_cdk import (
#     # Duration,
#     Stack,
#     # aws_sqs as sqs,
# )
# from constructs import Construct

# class PipelineStack(Stack):

#     def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
#         super().__init__(scope, construct_id, **kwargs)

#         # The code that defines your stack goes here

#         # example resource
#         # queue = sqs.Queue(
#         #     self, "PipelineQueue",
#         #     visibility_timeout=Duration.seconds(300),
#         # )

from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    Stage,
    Environment,
    pipelines,
    aws_codepipeline as codepipeline
)
from constructs import Construct
from resource_stack.resource_stack import ResourceStack


class DeployStage(Stage):
    def __init__(self, scope: Construct, id: str, env: Environment, **kwargs) -> None:
        super().__init__(scope, id, env=env, **kwargs)
        ResourceStack(self, 'ResourceStack', env=env, stack_name="resource-stack-deploy-latest")


class AwsCodepipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        git_input = pipelines.CodePipelineSource.connection( # source 
            repo_string="HiteshMakol/pipeline_new",
            branch="main",
            connection_arn="arn:aws:codestar-connections:ap-south-1:940394231405:connection/a8840bcc-0007-4122-8655-0e7504a4e132"
        )

        code_pipeline = codepipeline.Pipeline( # build
            self, "Pipeline",
            pipeline_name="new-pipeline-new",
            cross_account_keys=False
        )

        synth_step = pipelines.ShellStep( # synth
            id="Synth",
            install_commands=[
                'pip install -r requirements.txt'
            ],
            commands=[
                'npx cdk synth'
            ],
            input=git_input
        )

        pipeline = pipelines.CodePipeline(                                 ###### mutation true
            self, 'CodePipeline',
            self_mutation=True,
            code_pipeline=code_pipeline,
            synth=synth_step
        )

        deployment_wave = pipeline.add_wave("DeploymentWave")                  ##### deployment 

        deployment_wave.add_stage(DeployStage(
            self, 'DeployStage',
            env=(Environment(account='940394231405', region='ap-south-1'))
        ))
