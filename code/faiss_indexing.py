import faiss
import numpy as np

def create_index(embeddings_np):
    """Creates a FAISS index for similarity search."""
    dimension = embeddings_np.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings_np)
    return index

def retrieve_relevant_segments(query, index, all_segments, all_metadata, model, top_k=3):
    """Retrieves the most relevant text segments for a given query."""
    query_embedding = model.encode([query])
    _, indices = index.search(np.array(query_embedding, dtype='float32'), top_k)

    retrieved_segments = [all_segments[idx] for idx in indices[0]]
    retrieved_metadata = [all_metadata[idx] for idx in indices[0]]

    return retrieved_segments, retrieved_metadata
