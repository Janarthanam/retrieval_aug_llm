from fastapi import APIRouter, UploadFile, File
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
_db = vector_store.get_instance()
_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")

@router.post("/v1/docs")
async def index_doc(file: UploadFile = File(...)):
    async for doc in generate_documents(file):
        _db.add_documents([doc])
    #todo return something sensible
    return JSONResponse(status_code=200, content={})

@router.get("/v1/docs")
async def search(query: str):
    print(query)
    docs = _db.similarity_search(query=query)
    answer = _chain.run(input_documents=docs, question=query)
    return JSONResponse(status_code=200, content={"answer": answer}) 

async def generate_documents(file: UploadFile):
    num=0
    async for txt in convert_documents(file):
        num += 1
        document = Document(page_content=txt,metadata={"page": num})
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