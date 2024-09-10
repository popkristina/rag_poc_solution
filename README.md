# RAG for Technical Documentation

This repository contains the code and ideation for a RAG solution that is intended for use by technical staff. The project is in a POC phase so it is not fully functional.

## Proof of Concept
### 1. Objective of the POC

This solution should:

- Reduce time developers spend in documentation browsing.
- Provide accurate and up-to-date responses to developer queries.
- Assist developers who are unfamiliar with certain parts of the documentation.
- (Extra) Suggest further reading material based on the query.


### 2. Scope of the POC

- Data: The POC will utilize a subset of the available AWS documentation, which is public and has no usage limitations.
- Users: Initially implemented to access and test from one AWS account.
- Functionality: A pipeline that behaves as chatbot where a developer can input a query. The system should provide accurate responses by retrieving relevant sections from the AWS documentation and optionally, suggest further reading materials or related documents.

### 3. Technical Approach

#### **Data Ingestion:** 

Manually upload and store the AWS documentation data in the project's file system for easy access and manipulation, and optionally, store it in an S3 bucket for quick access.

#### **Data Preprocessing:**

#### Search and Retreival:

Develop a search algorithm to retrieve the most relevant sections of the documentation based on the query.
Implement a ranking mechanism to prioritize the most useful results.


Natural Language Processing (NLP):

    Implement NLP models to understand and process developer queries.
    Use pre-trained models like BERT or GPT for semantic search and context understanding.




## 4. Security and Compliance Considerations

- For the POC: Since the data is public AWS documentation, there are no security or compliance concerns.


## 5. Evaluation Criteria

Success Metrics:

    Reduction in time spent searching for documentation (measured through developer feedback or time-tracking).
    Accuracy of the system in retrieving relevant documentation.
    Reduction in the number of questions developers ask their peers.

User Feedback:

    Gather feedback from the team to refine the system before broader deployment.

## 6. Future Considerations

- Internal Documentation: Extend the system to include Company X's internal documentation while ensuring compliance with security and geographical restrictions.
- Advanced Features: Implement the nice-to-have features, such as advanced recommendations and contextual understanding, to further enhance the system.

# DEMO Usage


# Final System Requirements

## 1. OBJECTIVE

The objectives of the final system are the same as the one of the POC, except there should be another one included: Cost savings.

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