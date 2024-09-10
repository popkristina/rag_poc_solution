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

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('runtime.sagemaker')


# ARGUMENT PARSER #################################################


parser = argparse.ArgumentParser()
parser.add_argument("--input-data", type=str, dest='data_update',
                    help='data to update the knowledge base with')
parser.add_argument('--output', type=str, dest='prepped_data')
args = parser.parse_args()


# READ NEW DATA TO UPDATE VECTOR DATABASE WITH ###################


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


# TURN NEW DATA INTO VECTORS ##################################


# Preprocess first
html_removed_texts = df.apply(
    lambda row: (
        row['id'],
        remove_html_anchors(row['text'])), axis=1).tolist()

normalized_texts = [
    (item[0], normalize_text(item[1])) for item in html_removed_texts]


# TODO: Actually deploy model to make this piece of code work


def get_embeddings(text):
    # TODO: Move this function to utils with all
    # other functionalities

    response = sagemaker_runtime.invoke_endpoint(
        EndpointName='your-endpoint-name',
        ContentType='application/json',
        Body=json.dumps({"text": text})
    )
    result = json.loads(response['Body'].read().decode())
    return result
    

# Example usage
text = "Your sample text here"
embeddings = get_embeddings(text)
print(embeddings)


########## CONNECTION TO EXISTING VECTOR DATABASE ############




###### UPDATE VECTOR DATABASE WITH NEW KNOWLEDGE VECTORS ######



