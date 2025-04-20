import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv()


client = chromadb.PersistentClient()

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="text-embedding-ada-002",  # or another model
)


try:
    chroma_collection = client.get_collection(
        "med_records", embedding_function=openai_ef
    )
except ValueError:
    chroma_collection = client.create_collection(
        "med_records", embedding_function=openai_ef
    )


def insert_documents(docs: list[dict]):
    chroma_collection.add(
        ids=[doc["id"] for doc in docs],
        documents=[doc["text"] for doc in docs],
        metadatas=[doc["metadata"] for doc in docs],
    )
