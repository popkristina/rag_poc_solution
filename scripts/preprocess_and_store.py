import pandas as pd
import argparse
import boto3
import json

###################### ARGUMENT PARSER #######################

parser = argparse.ArgumentParser(description='Inputs for script.')
parser.add_argument('--new_data', dest='new_docs_path',
                    help='sum the integers (default: find the max)')

args = parser.parse_args()
print(args.accumulate(args.integers))


######## READ NEW DATA TO UPDATE VECTOR DATABASE WITH ########



################ TURN NEW DATA INTO VECTORS ##################

#TODO: Actually deploy model to make this piece of code work

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('runtime.sagemaker')


def get_embeddings(text):
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



