from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Body
from langchain.schema import Document
import io
import os
from pypdf import PdfReader
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from db.vector_store import Store

async def generate_documents(file: UploadFile, file_name: str):
    num=0
    async for txts in convert_documents(file):
        num += 1
        for txt in txts:
            document = Document(page_content=txt,metadata={"file": file_name, "page": num})
            yield document
 
async def convert_documents(file: UploadFile):
    splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0)

    #parse pdf document
    if file.content_type == 'application/pdf':
        content = await file.read()
        pdf_reader = PdfReader(io.BytesIO(content))
        try:
            for page in pdf_reader.pages:
                yield splitter.split_text(page.extract_text())
        except Exception as e:
            print(f"Exception {e}")
    elif "text" in file.content_type:
        content = await file.read()
        yield splitter.split_text(content.decode("utf-8"))
    else:
        return