#This is to init the vector store

from typing import Annotated

from db.vector_store import Store
from parsers.document_parsers import Parser

from fastapi import APIRouter, Body
from fastapi.responses import JSONResponse
from fastapi import APIRouter, UploadFile, File, Body

router = APIRouter()

@router.put("/v1/datasets")
async def recreate_collection(name: Annotated[str, Body(embed=True)]):
    """ Create a dataset with `name`. 
        **Delete and re-create if one exist.**

    Parameters:
        `name` of the doc to be created.
    Returns:
        None
    """
    print(f"creating collection {name} in db")
    return Store.get_instance().create_collection(name)

@router.post("/v1/datasets")
async def update(name: Annotated[str, Body()], file_name: Annotated[str, Body()], file: UploadFile = File(...)):
    """Update dataset `name` with information from the file.
    Paramters:
        `name` of the collection
        `file` to upload.
        `fileName` name of the file. This is used for metadata purposes only.
    Returns:
        name of the dataset once updated.
    """
    
    #TODO return meaningful info

    _db = Store.get_instance().get_collection(name)
    if not _db:
        return JSONResponse(status_code=404, content={})

    docs = await Parser.get_instance(file).parse(file, file_name)
    for doc in docs:
        print(doc)
        _db.add_documents([doc])
    return JSONResponse(status_code=200, content={"name": name})

