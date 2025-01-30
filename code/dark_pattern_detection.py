import os
import json
from config import MODEL, DATA_DIR, LOG_FILE, OUTPUT_DIR, TARGET_DP, client
from pdf_processing import process_all_pdfs, embedding_model
from faiss_indexing import create_index, retrieve_relevant_segments
from image_processing import encode_image
from log_utils import write_log

# Process PDFs and create FAISS index
all_segments, all_metadata, embeddings_np = process_all_pdfs("sources")
index = create_index(embeddings_np)

# Retrieve relevant segments
query = TARGET_DP
top_k = 1
retrieved_segments, retrieved_metadata = retrieve_relevant_segments(query, index, all_segments, all_metadata, embedding_model, top_k)

def format_citation(metadata):
    """Formats metadata for citations."""
    author = metadata.get("author", "Unknown Author")
    title = metadata.get("title", "Untitled Document")
    creation_date = metadata.get("creationDate", "n.d.")
    year = creation_date[2:6] if creation_date.startswith("D:") else "n.d."
    return f"({author}, {title}, {year})"

# Prompt
target_dp = "High Demand or Low Stock"
target_dp_description = "Uses Scarcity and Popularity Claims as Social Engineering to falsely suggest high demand or limited availability, pressuring users into uninformed purchases."
prompt = (
    "You are a helpful assistant that detects and reports dark patterns, i.e., deceptive design patterns, by giving the reasoning behind the decision!"
    "Inputs are screenshots of web pages. First of all, analyse the input and don't decide until the analysis is completed."
    "Analysis should follow these steps:"
    "1 - Detect measurable features which are observable, quantifiable elements."
    "For instance, \"accept all\" button is a visual entity while \"accept all\" text is a linguistic entity."
          "Metrics are the functions take the entity as an input and perform measuring."
          "For instance, 'size' is a metric which calculates weight and height in pixels."
          "Therefore, 'size of the accept all button' is a visual and measurable feature."
          "Another example is 'clarity of the accept all text'. In this case, 'clarity' is the metric."
          "Very important issue is that the metric's formula should be clear. If you say clarity, clarity formula should be clear, objective."
          "Now, please list all measurable features that can be relevant with dark patterns."
    "2 - Assess them and check if there is any asymmetric, restrictive, deceptive pattern, or hidden information that are the characteristics of dark patterns"
    f"3 - Analysis should be step by step. After determining the measurable features"
    f"Decide if there is a {target_dp} which is described as: {target_dp_description} and considering the retrieval context: {retrieved_segments}"
    "The output should have two components and be formed as below:"
    "Output 1: Label. It can be True or False."
    "Output 2: Explanation. It should contain the steps of your reasoning behind the previous output. Use the following example structure for the explanation."
    "1. Measurable Features:"
    "2. Assessment:"
    "3. Conclusion:"
    f"Add quote from: {retrieved_segments} and give the title and year info if available in the Output 2 by quoting. "
)

write_log(LOG_FILE, f"________________START________________\nPrompt: {prompt}")

# Process screenshots
results = []
for screenshot_file in os.listdir(DATA_DIR):
    if screenshot_file.endswith((".png", ".jpg")):
        image_path = os.path.join(DATA_DIR, screenshot_file)
        base64_image = encode_image(image_path)

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": [
                    {"type": "text", "text": "Is there any dark pattern on the given screenshot?"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
                ]}
            ],
            temperature=0.0,
        )

        analysis_result = response.choices[0].message.content
        output_1 = analysis_result.split("Output 2:")[0].split("Output 1:")[1].strip()
        output_2 = analysis_result.split("Output 2:")[1].strip()

        results.append({
            "screenshot": screenshot_file,
            "analysis_result": {"label": output_1, "explanation": output_2}
        })

        log_data = f"%%%%%%%%%%%%%%%\nAnalysis for {screenshot_file}:\n{analysis_result}\n"
        write_log(LOG_FILE, log_data)

# Save results to JSON
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_file = os.path.join(OUTPUT_DIR, f"{TARGET_DP}.json")

with open(output_file, 'w') as json_file:
    json.dump(results, json_file, indent=4)

print(f"Results saved to {output_file}")
