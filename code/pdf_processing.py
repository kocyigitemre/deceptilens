import os
import fitz  # PyMuPDF for PDF text and metadata extraction
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize the model for embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def extract_text_metadata(pdf_path):
    """Extracts text and metadata from a given PDF file."""
    doc = fitz.open(pdf_path)
    text_data = []
    metadata = doc.metadata  # Extract title, author, creation date if available

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text_data.append(page.get_text("text"))

    return "\n".join(text_data), metadata

def segment_and_embed(text):
    """Segments text into paragraphs and generates embeddings."""
    segments = text.split("\n\n")  # Split by paragraphs or sections
    embeddings = embedding_model.encode(segments)
    return segments, embeddings

def process_all_pdfs(folder_path):
    """Processes all PDFs in a given folder and returns text segments, metadata, and embeddings."""
    all_segments, all_metadata, all_embeddings = [], [], []

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(folder_path, filename)
            text, metadata = extract_text_metadata(pdf_path)
            segments, embeddings = segment_and_embed(text)

            all_segments.extend(segments)
            all_metadata.extend([metadata] * len(segments))  # Repeat metadata for each segment
            all_embeddings.extend(embeddings)

            print(f"Processed {filename} with {len(segments)} segments.")

    return all_segments, all_metadata, np.array(all_embeddings, dtype='float32')
