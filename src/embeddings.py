from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import pickle

# Load a pre-trained embedding model (MiniLM for efficiency)
model = SentenceTransformer("all-MiniLM-L6-v2")

def generate_embeddings(text_list):
    """Converts a list of text chunks into numerical embeddings."""
    embeddings = model.encode(text_list, convert_to_numpy=True)
    return embeddings

def store_embeddings_faiss(embeddings, file_path="data/faiss_index"):
    """Stores embeddings in FAISS for fast retrieval."""
    dimension = embeddings.shape[1]  # Must match the embedding size (384 for MiniLM)
    index = faiss.IndexFlatL2(dimension)  # L2 distance FAISS index
    index.add(embeddings)

    # Save FAISS index
    faiss.write_index(index, file_path)

    return index

def save_metadata(text_list, metadata_path="data/metadata.pkl"):
    """Saves the original text chunks for retrieval mapping."""
    with open(metadata_path, "wb") as f:
        pickle.dump(text_list, f)

# Example Usage
if __name__ == "__main__":
    sample_texts = [
        "The Eiffel Tower is located in Paris, France.",
        "Paris is the capital city of France.",
        "Artificial Intelligence is transforming industries."
    ]
    
    embeddings = generate_embeddings(sample_texts)
    faiss_index = store_embeddings_faiss(embeddings)
    save_metadata(sample_texts)
    
    print("Embeddings stored successfully!")