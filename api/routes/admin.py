#This is to init the vector store

from typing import Annotated

from qdrant_client.models import VectorParams, Distance
from fastapi import APIRouter, Body
from db import vector_store

router = APIRouter()

@router.put("/admin/v1/db")
async def recreate_collection(name: Annotated[str, Body(embed=True)]):
    print(f"creating collection {name} in db")
    return vector_store.client.recreate_collection(collection_name=name, 
                                            vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
