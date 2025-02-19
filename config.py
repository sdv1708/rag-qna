import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configuration class for the application """
    API_KEY = os.getenv("API_KEY")
    API_ENDPOINT = os.getenv("API_ENDPOINT")
    MODEL_NAME = os.getenv("MODEL_NAME")
    FAISS_INDEX_PATH = os.getenv("FAISS_INDEX_PATH")
    FAISS_METADATA_PATH = os.getenv("FAISS_METADATA_PATH")
    DOCUMENTS_PATH = os.getenv("DOCUMENT_FOLDER")