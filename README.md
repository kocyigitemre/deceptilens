# DeceptiLens
Note: The repository will be updated soon. 
## Introduction
In this project, we collected reported Dark Pattern / Deceptive Pattern (DP) screenshots from different sources, such as academic publications, reports and websites. 
We propose "DeceptiLens" as a robust and transparent DP detection approach. We employ multimodal-LLM, specifically GPT-4o, and apply RAG to minimize incorrect outputs. DeceptiLens is not only for capturing DPs in the UI, but also providing explanation about the reasoning behind each identification process. We utilize prompting techniques, such as Chain-of-Thought (CoT), and instruct the model for a certain output structure. Dark Pattern experts evaluated the AI-generated explanations in terms of "clarity", "correctness", "completeness" and "verifiability", in a 1-5 scale. The results will be presented at ACM FAccT 2025, and the paper link will shared soon.

## Datasets
### 1. Input data
All of the collected data (a collection of screenshots) is available under the "data" folder.
### 2. Model's classification and explanations
Classification of the input data with explanations is available under the "model-output" folder.
### 3. Experts' classification
Classification of the input data by experts. Each example was evaluated by three different experts. 


## Code
### 1. Configuration 
Openai model selection and directory arrangement can be done by "config.py" file.
You should add your API KEY to the api-key.txt file.
Embedding model in the RAG process can be modified by "pdf_processing.py" file.
### 2. Main
"dark_pattern_detection.py" is the main file, and target dark pattern category and its description should be updated accordingly.
Classification of the given UI and explanation about the reasoning of the model will be stored in a .json file after running the main file.
