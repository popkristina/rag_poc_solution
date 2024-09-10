# Note: This script is intended to show how the process would
# look like and is not indended to run at this point

import pandas as pd
import argparse
import boto3
import json
from utils import *
from io import StringIO  

###################### ARGUMENT PARSER #######################


"""
In case we want to update the knowledge base with fresh documents,
we give a path to where the new documents are. 
We also give a path to where we want to store  the preprocessed
and chunked files.
"""
parser = argparse.ArgumentParser()
parser.add_argument("--input-data", type=str, dest='data_update', 
                    help='data to update the knowledge base with')
parser.add_argument('--output', type=str, dest='prepped_data')
args = parser.parse_args()


######## READ NEW DATA TO UPDATE VECTOR DATABASE WITH #########

new_files_path = args.data_update

# TODO: Implement additional file format checks in case 
# not all documents are .md format
md_files = glob.glob(os.path.join(new_files_path, '*.md'))
df = read_glob_files(md_files)

# Upload data to S3 bucket 
# Not tested if this will work

csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

s3_resource = boto3.resource('s3')
s3_resource.Object(
    'sagemaker-studio-863518450685-ozz0puftsu9', 
    'data/new_raw_documents/documents.csv').put(Body=csv_buffer.getvalue())


################ TURN NEW DATA INTO VECTORS ##################

#TODO: Actually deploy model to make this piece of code work

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('runtime.sagemaker')


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




###### UPDATE VECTOR DATABASE WITH NEW KNOLEDGE VECTORS ######



