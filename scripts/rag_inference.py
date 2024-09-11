"""
v01: Initial concept of the process

Here we want to concatenate the input query and the
input context from most similar documents and send
them to the LLM to generate response.

"""

import pandas as pd
import argparse
import boto3
import json
import os
import glob
from datetime import datetime
from utils import *
from io import StringIO


#  DEFINE GLOBAL VARIABLES #########################################


# Initialize a SageMaker runtime client
sagemaker_runtime = boto3.client('sagemaker-runtime')
endpoint_name = 'endpoint-name-to-falcon-model'  


#  DEFINE FUNCTIONS ################################################


def query_llm_model(endpoint_name, query_text):
    """
    Parameters
    ----------
    endpoint_name: String
        The name of the endpoint for the deployed LLM
    query_text: String
        The full query with context to be sent to the LLM

    Returns
    -------
    json:
        The answer from the model
    """
    
    # Prepare the payload for the model
    payload = {"inputs": query_text}
    payload_json = json.dumps(payload)

    # Invoke the endpoint
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=payload_json
    )

    # Read the response and convert to json
    response_body = response['Body'].read().decode('utf-8')
    result = json.loads(response_body)
    return result


# ARGUMENT PARSER ##################################################


parser = argparse.ArgumentParser()
parser.add_argument("--input-query", type=str, dest='user_query',
                    help='the original user query')
parser.add_argument("--input_context", type=str, dest='context_str',
                    help='the most similar documents')
args = parser.parse_args()


# READ INPUT DATA ##################################################


# Read input query
user_query = args.user_query

# Read context
with open(args.context_str, 'r') as f:
    context_data = json.load(f)
    
# Concatenate query with context
full_query = user_query
docs = context_data['top_5_similar_docs']
for doc in docs:
    full_query += '\n' + doc


# SEND NEW INPUT TO LLM #############################################


# Save the output of Step 2
with open(args.output_path, 'w') as f:
    json.dump(output_data, f)

response = query_falcon_model(endpoint_name, full_query)
print("Model Response:\n", response)

