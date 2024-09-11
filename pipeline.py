import sagemaker
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.workflow.parameters import ParameterString
from sagemaker.processing import ScriptProcessor, ProcessingOutput

# Define parameters
input_query = ParameterString(name="InputQuery", default_value="input_query")
output_path = "data/preprocessed/tmp_retreived"
ROLE_ARN = 'arn:aws:iam::863518450685:role/service-role/AmazonSageMaker-ExecutionRole-20240908T121797'
INSTANCE_TYPE = 'ml.t3.medium'
S3_BUCKET = 'sagemaker-studio-863518450685-ozz0puftsu9'
RAW_DATA_S3_KEY = 'data/raw'
PROCESSED_DATA_S3_KEY = 'data/processed/text_with_embeddings.csv'


# Define the processing scripts

steps_processor = ScriptProcessor(
    role="ROLE_ARN",
    command=["python3"],
    instance_type="INSTANCE_TYPE",
    instance_count=1
)


# Step 1: Encode query and find similar documents

"""
First step should call a script that takes
the user query as input, and outputs the top
K most similar documents.
"""

step1_output = ProcessingOutput(
    output_name="step1_output",
    source="/opt/ml/processing/output")

step1 = ProcessingStep(
    name="Encode and search vector base",
    processor=steps_processor,
    outputs=[step1_output],
    code="scripts/search_and_retreive.py",
    job_arguments=[
        "--input-query", input_query,
        "--bucket-name", S3_BUCKET,
        "--output", output_path]
)

# Step 2: RAG Inference
"""
Second step should call a script that takes as
inputs the original query and the most similar
documents, concatenates them and sends them to
the LLM, then it outputs the answer to the query.
"""
step2 = ProcessingStep(
    name="Add context to query and generate output",
    processor=steps_processor,
    inputs=[step1_output],
    outputs=[],
    code="scripts/rag_inference.py",
    job_arguments=[
        "--input_string", input_query,
        "--input_context", output_path]
)

# Define the pipeline
pipeline = Pipeline(
    name="MyPipeline",
    parameters=[input_query],
    steps=[step1, step2]
)

if __name__ == "__main__":
    pipeline.upsert(role_arn=ROLE_ARN)
    execution = pipeline.start(parameters={"InputQuery": "How are you today?"})
    execution.wait()
