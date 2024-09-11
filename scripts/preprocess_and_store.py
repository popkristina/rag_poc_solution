"""
v01: Initial concept of the process

In case we want to update the knowledge base with fresh
documents, we give a path to where the new documents are.

We also give a path to where we want to store the
preprocessed and chunked files.

In the POC, these files are stored in our project file
system as we have no restrictions on the public data usage.

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
bucket_name = 'sagemaker-studio-863518450685-ozz0puftsu9'

# Abritrary that would be created within bucket
preprocessed_path_s3 = f'data/new_raw_documents/docs_{upld_date}.csv'
path_vector_database = 'data/vector_embeddings.csv'

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('runtime.sagemaker')


#  DEFINE FUNCTIONS ################################################


def get_embeddings(text):
    # TODO: Deploy before using this function

    response = sagemaker_runtime.invoke_endpoint(
        EndpointName='endpoint-for-all-MiniLM-L6-v2e',
        ContentType='application/json',
        Body=json.dumps({"text": text})
    )
    result = json.loads(response['Body'].read().decode())
    return result


# ARGUMENT PARSER ##################################################


parser = argparse.ArgumentParser()
parser.add_argument("--input-data", type=str, dest='data_update',
                    help='data to update the knowledge base with')
parser.add_argument('--output', type=str, dest='prepped_data')
args = parser.parse_args()


# READ NEW DATA TO UPDATE VECTOR DATABASE WITH ####################


new_files_path = args.data_update

# TODO: Implement additional file format checks in case
#       not all documents are .md format

# TODO: Update to read from alternative sources according
#       to business demand

md_files = glob.glob(os.path.join(new_files_path, '*.md'))
df = read_glob_files(md_files)

# Uploads data to S3 bucket (Not tested if this will work)
# This uploads prior to preprocessing, but uploads new
#      data as one file easier to access.
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

s3_resource.Object(
    bucket_name, preprocessed_path_s3
).put(Body=csv_buffer.getvalue())


# TURN NEW DATA INTO VECTORS ####################################


# Preprocess, normalize and chunk data first
processed_data = []

for index, row in df.iterrows():
    doc_id = row['id']
    text = row['text']

    cleaned_text = normalize_text(remove_html_anchors(text))
    chunks = split_text_by_tokens(cleaned_text)

    for chunk in chunks:
        processed_data.append({'doc_id': doc_id, 'text': chunk})

transformed_df = pd.DataFrame(processed_data)
transformed_df.insert(0, 'id', range(len(transformed_df)))

# And now encode texts
# Note: The code should use a deployed version of all-MiniLM-L6-v2
#       model which is available to deploy through JumpStart and
#       compatible with the SentenceTransformer wrapped function
#       for all-MiniLM-L6-v2 run through the notebook
encoded_texts = []
for index, row in transformed_df.iterrows():
    encoded_texts.append(get_embeddings(row['text']))
transformed_df['embeddings'] = encoded_texts


# CONNECTION TO EXISTING VECTOR DATABASE ########################


# No database in poc, just open file from S3 location
vector_res_object = s3_resource.get_object(
    Bucket=bucket_name, Key=path_vector_database)
vector_database = vector_res_object['Body'].read().decode('utf-8')
vector_df = pd.read_csv(StringIO(vector_database))


# UPDATE VECTOR DATABASE WITH NEW KNOWLEDGE VECTORS #############

vector_df = pd.concat([vector_df, transformed_df],
                      ignore_index=True)

# We can additionally clean the dabatase of duplicates depending
#  on whether the system logic requires it

# Now save the final dataframe back again
csv_buffer = StringIO()
vector_df.to_csv(csv_buffer, index=False)

s3_resource.Object(
    bucket_name, path_vector_database
).put(Body=csv_buffer.getvalue())


