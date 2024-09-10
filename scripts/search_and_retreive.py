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
bucket_name = 'sagemaker-studio-863518450685-ozz0puftsu9'

# Abritrary that would be created within bucket
path_vector_database = 'data/vector_embeddings.csv'

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('runtime.sagemaker')


#  DEFINE FUNCTIONS ################################################


def find_top_5_similar_docs(query_vector, doc_vectors_df):
    """
    A function that accepts a query vector and a dataframe
    of query vectors, compares the query vector to all other
    vectors in the dataframe based on cosine similarity and 
    returns the top 5 with the highest similarity.

    Parameters
    ----------
    query_vector: String
        The user query we are looking similarities with
    doc_vectors_df: pd.DataFrame
        The document index which maps each document to 
        a vector embedding.
    Returns
    -------
    List, List
        A list of top 5 most similar documents and a list
        of their corresponding top 5 similarities.
    """

    similarities = []

    # Iterate through each document in the DataFrame
    for index, row in doc_vectors_df.iterrows():
        doc_vector = row.drop('text').values  
        similarity = cosine_similarity(query_vector, doc_vector)
        similarities.append((index, similarity))

    # Sort by similarity in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)

    # Extract top 5 documents
    top_5_indices = [
        index for index, similarity in similarities[:5]]
    top_5_similarities = [
        similarity for index, similarity in similarities[:5]]
    top_5_texts = [
        doc_vectors_df.at[index, 'text'] for index in top_5_indices]

    return top_5_texts, top_5_similarities


# ARGUMENT PARSER ##################################################


parser = argparse.ArgumentParser()
parser.add_argument("--input-query", type=str, dest='user_query',
                    help='a query the user types in to ask something')
parser.add_argument('--output', type=str, dest='prepped_data')
args = parser.parse_args()


# CONNECTION TO EXISTING VECTOR DATABASE ###########################


# Dataframe with vector embeddings to compare by similarity with
vector_res_object = s3_resource.get_object(
    Bucket=bucket_name, Key=path_vector_database)
vector_database = vector_res_object['Body'].read().decode('utf-8')
vector_df = pd.read_csv(StringIO(vector_database))


# COMPARE SIMILARITIES #############################################


query = args.user_query
top_5_texts, _ = find_top_5_similar_docs(query, vector_df)

