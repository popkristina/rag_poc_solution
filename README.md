# RAG for Technical Documentation

This repository contains the code and ideation for a RAG solution that is intended for use by technical staff. The project is in a POC phase so it is not fully functional.

# Proof of Concept
## 1. Objective of the POC

This solution should:

- Reduce time developers spend in documentation browsing.
- Provide accurate and up-to-date responses to developer queries.
- Assist developers who are unfamiliar with certain parts of the documentation.
- (Extra) Suggest further reading material based on the query.


## 2. Scope of the POC

- **Data**: The POC will utilize a subset of the available AWS documentation, which is public and has no usage limitations.
- **Users**: Initially implemented to access and test from one AWS account.
- **Functionality**: A pipeline that behaves as chatbot where a developer can input a query. The system should provide accurate responses by retrieving relevant sections from the AWS documentation and optionally, suggest further reading materials or related documents.

## 3. Technical Approach

### Data Ingestion

Manually upload and store the AWS documentation data in the project's file system for easy access and manipulation, and optionally, store it in an S3 bucket for quick access.

### Storage

File system and optionally, S3 bucket storage for knowledge data in vector format.

### Data Preprocessing

- **Text Cleaning**: Clean text from HTML-like elements, as well as those indicating images.
- **Text Normalization**: Normalize special characters that show up typucally in .md files.
- **Text Chunking**: Chunking is performed so that each chunk of text will fit the maximum number of tokens that the embedding model accepts. In this proposed solution, it is 256 tokens. The leftovers from every document are added to a next chunk.

###   
### Search and Retreival

Develop a search algorithm to retrieve the most relevant sections of the documentation based on the query.
Implement a ranking mechanism to prioritize the most useful results.

### Model Choice 



## 4. Security and Compliance Considerations

Since the initial dataset is public AWS documentation, there are no security or compliance concerns to its usage.


## 5. Evaluation Criteria

Success Metrics:

    Reduction in time spent searching for documentation (measured through developer feedback or time-tracking).
    Accuracy of the system in retrieving relevant documentation.
    Reduction in the number of questions developers ask their peers.

User Feedback:

    Gather feedback from the team to refine the system before broader deployment.

## 6. Limitations of POC

- Does not have a trigger of when the public documentation is updated. Updating of knowledge base with vectors should be invoked manually through a notebook.
- Does have a vector embedding model deployed on Sagemaker to avoid incurring additional costs.

# DEMO Usage

## 1. Project Structure


    loka_rag_solution/
    ├── data/
    │   └── raw/
    │   └── preprocessed/
    ├── notebooks/
    ├── scripts/
    │   ├── utils.py                    # contains helper functions for data manipulation
    │   ├── preprocess_and_store.py     # updates vector knowledge base with new data
    │   ├── search_and_retreive.py      # looks up most similar vectors to a query vector
    │   └── rag_inference.py            # collects all relevant input and sends to llm 
    ├── requirements.txt
    ├── pipeline.py
    └── README.md

# Final System Requirements

## 1. OBJECTIVE

The objectives of the final system are the same as the one of the POC, except there should be another one included: **Cost savings**.

In order to achieve cost savings, the following should be true:

$$ Cost(hours of labor to develop solution) + Cost(hours of labor to maintain solution) + Cost(API calls to LLM on AWS) + Cost(Storage) < Cost(hours of labor in searching through documentation instead of working on other profitable projects)$$

## 2. 

Security

- For the final system:

    Implement access controls and encryption to protect sensitive internal documentation.
    Ensure compliance with geographical restrictions (e.g., data must not leave the US).
    Implement role-based access to ensure that only authorized users can access proprietary information.


  (Optional) Recommendation System:

    Implement a simple recommendation engine that suggests related documents or sections for further reading.