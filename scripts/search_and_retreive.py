"""
v01: Initial concept of the process

The script should accept a query as an input and
return the most similar documents concatenated to it.

Script is not complete and will not work as such.

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


# Get current date
upld_date = datetime.today().strftime("%m%d%Y")

# Necessary vars for s3 bucket connection
s3_resource = boto3.resource('s3')

# Abritrary that would be created within bucket
path_vector_database = 'data/vector_embeddings.csv'

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('runtime.sagemaker')


#  DEFINE FUNCTIONS ################################################


def get_embeddings(text):
    # Note: This model is not deployed and this
    #       function cannot be used until it is.
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName='endpoint-for-all-MiniLM-L6-v2e',
        ContentType='application/json',
        Body=json.dumps({"text": text})
    )
    result = json.loads(response['Body'].read().decode())
    return result


# ARGUMENT PARSER ##################################################


parser = argparse.ArgumentParser()
parser.add_argument("--input-query", type=str, dest='user_query',
                    help='a query the user types in to ask something')
parser.add_argument("--bucket-name", type=str, dest='bucket_name',
                    help='system name of the s3 bucket')
parser.add_argument('--output', type=str, dest='prepped_data')
args = parser.parse_args()


# CONNECTION TO EXISTING VECTOR DATABASE ###########################


# Dataframe with vector embeddings to compare by similarity with
vector_res_object = s3_resource.get_object(
    Bucket=args.bucket_name, Key=path_vector_database)
vector_database = vector_res_object['Body'].read().decode('utf-8')
vector_df = pd.read_csv(StringIO(vector_database))


# COMPARE SIMILARITIES #############################################


query = args.user_query
embedded_query = get_embeddings(query)
top_5_texts, _ = find_top_5_similar_docs(query, vector_df)


# SAVE THE OUTPUT LIST #############################################

output_list = {
    "query": query,
    "top_5_similar_docs": top_5_texts
}

# Save the output list to the specified path
with open(args.output_path, 'w') as f:
    json.dump(output_list, f)

print(f"Output saved to {args.output_path}")