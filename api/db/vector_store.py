from abc import abstractmethod
import os
from qdrant_client import QdrantClient
from langchain.embeddings import OpenAIEmbeddings, ElasticsearchEmbeddings
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Qdrant, ElasticVectorSearch, VectorStore
from qdrant_client.models import VectorParams, Distance


class ToyVectorStore:

    @staticmethod
    def get_embedding():
        embedding = os.getenv("EMBEDDING")
        if "SENTENCE" == embedding:
            return SentenceTransformerEmbeddings()
        elif "ELASTIC" == embedding:
            return ElasticsearchEmbeddings()
        else:
            return OpenAIEmbeddings()

    @staticmethod
    def get_instance():
        vector_store = os.getenv("STORE")

        if vector_store == "ELASTIC":
            return ElasticVectorStore(ToyVectorStore.get_embedding())
        elif vector_store == "QDRANT":
            return QdrantVectorStore(ToyVectorStore.get_embedding())
        else:
            raise ValueError(f"Invalid vector store {vector_store}")
    

    def __init__(self, embeddings):
        self.embeddings = embeddings

    @abstractmethod
    def get_collection(self, collection: str="test") -> VectorStore:
        """
        get an instance of vector store
        of collection
        """
        pass
    
    @abstractmethod
    def create_collection(self, collection: str) -> None:
        """
        create an instance of vector store
        with collection name
        """
        pass

class ElasticVectorStore(ToyVectorStore):

    def get_collection(self, collection:str) -> ElasticVectorSearch:
        return ElasticVectorSearch(elasticsearch_url= os.getenv("ES_URL"),
                               index_name= collection, embedding=self.embeddings)

    def create_collection(self, collection: str) -> None:
        store = self.get_collection(collection)
        store.create_index(store.client,collection, dict())


class QdrantVectorStore(ToyVectorStore):

    def __init__(self):
        self.client = QdrantClient(url=os.getenv("QDRANT_URL"),
                                        api_key=os.getenv("QDRANT_API_KEY"))

    def get_collection(self, collection: str) -> Qdrant:  
        return Qdrant(client=self.client,collection_name=collection,
                      embeddings=self.embeddings)

    def create_collection(self, collection: str) -> None:
        self.client.create_collection(collection_name=collection, 
                        vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
    