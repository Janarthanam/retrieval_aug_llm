#This is to init the vector store

from typing import Annotated

from fastapi import APIRouter, Body
from db.vector_store import ToyVectorStore

router = APIRouter()

@router.put("/admin/v1/db")
async def recreate_collection(name: Annotated[str, Body(embed=True)]):
    """ `name` of the collection to be created.
    If one exits, delete and recreate.
    """
    print(f"creating collection {name} in db")
    return ToyVectorStore.get_instance().create_collection(name)