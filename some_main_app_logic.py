import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.processing import ScriptProcessor
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
import config

# Note: Pipeline part of logic where we update the knowledge
# base is not implemented


# Define the processing step
processor = ScriptProcessor(
    image_uri='682000322983.dkr.ecr.us-west-2.amazonaws.com/sklearn-0.20.0-cpu-py3',
    command=['python3'],
    instance_type=config.INSTANCE_TYPE,
    instance_count=1,
    base_job_name='preprocess-data',
    role=config.ROLE_ARN,
)

preprocess_step = ProcessingStep(
    name='PreprocessData',
    processor=processor,
    code='scripts/preprocessing.py',
    inputs=[ProcessingInput(source=f's3://{config.S3_BUCKET}/{config.RAW_DATA_S3_KEY}', destination='/opt/ml/processing/input')],
    outputs=[ProcessingOutput(source='/opt/ml/processing/output', destination=f's3://{config.S3_BUCKET}/{config.PROCESSED_DATA_S3_KEY}')],
)

# Define the training step
estimator = Estimator(
    image_uri='763104351884.dkr.ecr.us-west-2.amazonaws.com/tensorflow-training:2.3.1-gpu-py37-cu110-ubuntu18.04',
    role=config.ROLE_ARN,
    instance_count=1,
    instance_type=config.INSTANCE_TYPE,
    output_path=f's3://{config.S3_BUCKET}/output/',
    base_job_name='train-model'
)

train_step = TrainingStep(
    name='TrainModel',
    estimator=estimator,
    inputs={
        'train': TrainingInput(s3_data=f's3://{config.S3_BUCKET}/{config.PROCESSED_DATA_S3_KEY}', content_type='csv')
    }
)

# Define and execute the pipeline
pipeline = Pipeline(
    name='MyPipeline',
    steps=[preprocess_step, train_step],
)

pipeline.upsert(role_arn=config.ROLE_ARN)
execution = pipeline.start()
execution.wait()