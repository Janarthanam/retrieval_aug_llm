import os
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

embeddings = OpenAIEmbeddings()
client = QdrantClient(url=os.getenv("QDRANT_URL"),
                                    api_key=os.getenv("QDRANT_API_KEY"))

def get_instance(collection: str = "test"):
    return Qdrant(client=client,collection_name=collection,embeddings=embeddings)

