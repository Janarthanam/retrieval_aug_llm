from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Body
from fastapi.responses import JSONResponse
import openai
import io
import os
from pypdf import PdfReader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from db import vector_store

router = APIRouter()
_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff", verbose=True)

@router.post("/v1/docs")
async def create_or_update(name: Annotated[str, Body()], file_name: Annotated[str, Body()], file: UploadFile = File(...)):
    """create or update a collection 
    `name` of the collection
    `file` to upload.
    `fileName` name of the file.
    """

    _db = vector_store.get_instance(name)
    if not _db:
        return JSONResponse(status_code=404, content={})
    async for doc in generate_documents(file, file_name):
        print(doc)
        _db.add_documents([doc])

    #todo return something sensible
    return JSONResponse(status_code=200, content={"name": name})

@router.get("/v1/doc/{name}/answer")
async def answer(name: str, query: str):
    """ Answer a question from the collection
    `name` of the collection.
    `query` to be answered.
    """
    _db = vector_store.get_instance(name)
    print(query)
    docs = _db.similarity_search(query=query)
    print(docs)
    answer = _chain.run(input_documents=docs, question=query)
    return JSONResponse(status_code=200, content={"answer": answer, "files": [d.metadata["file"] for d in docs]}) 

async def generate_documents(file: UploadFile, file_name: str):
    num=0
    async for txt in convert_documents(file):
        num += 1
        document = Document(page_content=txt,metadata={"file": file_name, "page": num})
        yield document
 
async def convert_documents(file: UploadFile):
    #parse pdf document
    if file.content_type == 'application/pdf':
        content = await file.read()
        pdf_reader = PdfReader(io.BytesIO(content))
        try:
            for page in pdf_reader.pages:
                yield page.extract_text()
        except Exception as e:
            print(f"Exception {e}")
    else:
        return