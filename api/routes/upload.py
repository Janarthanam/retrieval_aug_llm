#This is to init the vector store

from typing import Annotated

from db.vector_store import Store
from document_parsing import generate_documents

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, Body

router = APIRouter()

@router.put("/v1/docs")
async def recreate_collection(name: Annotated[str, Body(embed=True)]):
    """ `name` of the doc to be created.
    If one exits, delete and recreate.
    """
    print(f"creating collection {name} in db")
    return Store.get_instance().create_collection(name)

@router.post("/v1/docs")
async def update(name: Annotated[str, Body()], file_name: Annotated[str, Body()], file: UploadFile = File(...)):
    """Update an existing document with information from the file.
    If one doesn't exist with name, it creates a new document to update. 
    `name` of the collection
    `file` to upload.
    `fileName` name of the file. This is used for metadata purposes only.
    """
    
    _db = Store.get_instance().get_collection(name)
    if not _db:
        return JSONResponse(status_code=404, content={})

    async for doc in generate_documents(file, file_name):
        print(doc)
        _db.add_documents([doc])
    return JSONResponse(status_code=200, content={"name": name})

