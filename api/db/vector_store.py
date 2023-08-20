from abc import abstractmethod
from functools import cache
import os
from qdrant_client import QdrantClient
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Qdrant, ElasticVectorSearch, VectorStore
from qdrant_client.models import VectorParams, Distance
from db.embedding import Embedding, EMBEDDINGS


class Store:

    @staticmethod
    def get_embedding():
        embedding = os.getenv("EMBEDDING")
        if not embedding:
            return EMBEDDINGS["OPEN_AI"]
        return EMBEDDINGS[embedding]
    
    @staticmethod
    @cache
    def get_instance():
        vector_store = os.getenv("STORE")

        if vector_store == "ELASTIC":
            return ElasticVectorStore(Store.get_embedding())
        elif vector_store == "QDRANT":
            return QdrantVectorStore(Store.get_embedding())
        else:
            raise ValueError(f"Invalid vector store {vector_store}")
    

    def __init__(self, embedding: Embedding):
        self.embedding = embedding

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

    @abstractmethod
    def list_collections(self) -> list[dict]:
        """
        Return a list of collections in the vecot store.
        """
        pass

class ElasticVectorStore(Store):
    def __init__(self, embeddings):
        super().__init__(embeddings)

    def get_collection(self, collection:str) -> ElasticVectorSearch:
        return ElasticVectorSearch(elasticsearch_url= os.getenv("ES_URL"),
                               index_name= collection, embedding=self.embedding.embedding)
    
    def create_collection(self, collection: str) -> None:
        store = self.get_collection(collection)
        store.create_index(store.client,collection, dict())

    def list_collections(self) -> list[dict]:
        #TODO: not impelented
        return []

class QdrantVectorStore(Store):

    def __init__(self, embeddings):
        super().__init__(embeddings)
        self.client = QdrantClient(url=os.getenv("QDRANT_URL"),
                                        api_key=os.getenv("QDRANT_API_KEY"))

    def get_collection(self, collection: str) -> Qdrant:  
        return Qdrant(client=self.client,collection_name=collection,
                      embeddings=self.embedding.embedding)

    def create_collection(self, collection: str) -> None:
        self.client.create_collection(collection_name=collection, 
                        vectors_config=VectorParams(size=self.embedding.dimension, 
                                                    distance=Distance.COSINE))
    
    def list_collections(self) -> list[dict]:
        """ return a list of collections.
        """
        return [ c for i,c in enumerate(self.client.get_collections().collections)]
    