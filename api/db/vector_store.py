import os
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

embeddings = OpenAIEmbeddings()
client = QdrantClient(url="https://32f125d3-5ab1-4058-a10a-bd38a1ebd647.us-east-1-0.aws.cloud.qdrant.io",
                                    api_key=os.getenv("QDRANT_API_KEY"))

def get_instance(collection: str = "test"):
    return Qdrant(client=client,collection_name=collection,embeddings=embeddings)
