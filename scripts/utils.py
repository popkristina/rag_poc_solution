import re
import numpy as np
import pandas as pd
import os


def extract_relevant_sections(text):
    """
    Not used currently.

    Extract headings, code blocks, 
    and text sections.

    Parameters
    ----------
    text: String
        A piece of preprocessed text.

    Returns
    -------
    List
        A list of strings whereas each 
        string is a separate section.
    """
    sections = []

    # Match headings (e.g., # Heading, ## Subheading)

    heading_pattern = re.compile(r'^(#{1,6})\s+(.+)', re.MULTILINE)
    sections.extend(heading_pattern.findall(text))

    # Match code blocks (```...```)
    code_block_pattern = re.compile(r'```(.*?)```', re.DOTALL)
    sections.extend(code_block_pattern.findall(text))

    # Extract the remaining text
    remaining_text = re.sub(heading_pattern, '', text)
    remaining_text = re.sub(code_block_pattern, '', remaining_text)
    sections.extend(remaining_text.strip().splitlines())

    return sections


def cosine_similarity(vec1, vec2):
    """
    Calculate the cosine similarity between two 
    vector embeddings.

    Parameters
    ----------
    vec1: np.Array
        A numpy array representing the first vector embedding
    vec2: np.Array:
        A numpy array representing the second vector embedding

    Returns
    -------
    Float:
        Cosine similarity in range [-1, 1]
    """
    # Ensure the vectors are numpy arrays
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    # Compute the dot product between the two vectors
    dot_product = np.dot(vec1, vec2)

    # Compute the L2 norms (magnitudes) of the vectors
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    # Calculate the cosine similarity
    cosine_sim = dot_product / (norm_vec1 * norm_vec2)

    return cosine_sim


def remove_html_anchors(text):
    """
    Remove HTML anchor tags from 
    the markdown content.

    Parameters
    ----------
    text: String
        Original document in form of string

    Returns
    -------
    String
        Same string document without html
    """
    return re.sub(r'<a name="[^>]+"></a>', '', text)


def normalize_text(text):
    """
    Convert text to lowercase and 
    replace special characters.

    Parameters
    ----------
    text: String
        Document in form of string

    Returns
    -------
    String
        Normalized document in form of string
    """
    text = text.lower()
    text = re.sub(r'\\\.', '.', text)
    text = re.sub(r'\\\(', '(', text)
    text = re.sub(r'\\\)', ')', text)
    return text


def split_text_by_tokens(text, max_tokens=256):
    """
    Accepts a text and splits it into chunks such
    that each chunk will have the maximum number 
    of word-like tokens accepted by the embedding 
    model.

    If the chunk length exceeds the maximum length
    then the token is added to the next chunk.

    Parameters
    ----------
    text: String
        The preprocessed and normalized document
    max_tokens: Integer
        The maximum tokens accepted as sequence length
        in the embedding model

    Returns
    -------
    List:
        A list of strings that represend the chunks
        of the original text.
    """
    tokens = text.split()

    # Initialize variables
    chunks = []
    current_chunk = []

    for token in tokens:
        # If adding this token exceeds the limit, save the current 
        # chunk and tart a new one
        if len(current_chunk) + 1 > max_tokens:
            chunks.append(' '.join(current_chunk))
            current_chunk = [token]
        else:
            current_chunk.append(token)

    # Add the last chunk if there's remaining content
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


def read_glob_files(md_files):
    """
    Accepta a list of files retreived by
    glob.

    Parameters
    ----------
    md_files: List
        A list of paths to every document
        in the input folder.

    Returns
    -------
    pd.DataFrame
        A dataframe of documents
    """
    data = []
    for file in md_files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            doc_name = os.path.splitext(os.path.basename(file))[0]
            data.append({'id': doc_name, 'text': content})

    df = pd.DataFrame(data)
    return df


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

