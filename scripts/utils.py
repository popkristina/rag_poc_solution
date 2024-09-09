import re
import numpy as np


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