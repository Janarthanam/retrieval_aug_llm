#This is to init the vector store

from qdrant_client.models import VectorParams, Distance
from fastapi import APIRouter
from db import vector_store

router = APIRouter()

@router.put("/admin/v1/db")
async def recreate_collection(name: str = "test"):
    print(f"creating collection {name} in db")
    return vector_store.client.recreate_collection(collection_name=name, 
                                            vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
