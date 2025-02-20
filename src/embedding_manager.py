from sentence_transformers import SentenceTransformer
import faiss
import pickle
from config import app_config

class EmbeddingManager:
    """Handles embedding generation, FAISS storage and retrieval"""

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index_path = app_config.FAISS_INDEX_PATH
        self.metadata_path = app_config.FAISS_METADATA_PATH
        self.index = None

    def generate_embeddings(self, text_list):
        """Generate embeddings for a list of text chunks"""
        return self.model.encode(text_list, convert_to_numpy = True)
    
    def store_faiss_embeddings(self, embeddings, text):
        """Stores embeddings in FAISS and saves metadata"""
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        faiss.write_index(self.index, self.index_path)

        with open(self.metadata_path, "wb") as file:
            pickle.dump(text, file)
    
    def load_index(self):
        """Load the FAISS index from disk"""
        self.index = faiss.read_index(self.index_path)
        with open(self.metadata_path, "rb") as file:
            self.texts = pickle.load(file)
    
    def retrieve_similar_documents(self, query_text, top_k=None):
        """Retrieve similar documents using FAISS"""
        if self.index is None:
            self.load_index()
        query_embedding = self.generate_embeddings([query_text])
        distances, indices = self.index.search(query_embedding, top_k)

           
