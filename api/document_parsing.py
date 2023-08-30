from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Body
from langchain.schema import Document
import io
import os
from pypdf import PdfReader
from langchain.text_splitter import SentenceTransformersTokenTextSplitter

from doctr.io import DocumentFile
from doctr.models import ocr_predictor

predictor = ocr_predictor(pretrained = True)

def generate_documents(file: UploadFile, file_name: str):
    num=0
    for txts in convert_documents(file):
        num += 1
        for txt in txts:
            document = Document(page_content=txt,metadata={"file": file_name, "page": num})
            yield document
 
def convert_documents(file: UploadFile):
    splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0)

    #parse pdf document
    if file.content_type == 'application/pdf':
        content = file.read()
        pdf_reader = PdfReader(io.BytesIO(content))
        try:
            for page in pdf_reader.pages:
                txt = page.extract_text()
                if not txt:
                    return None
                yield splitter.split_text(txt)
        except Exception as e:
            print(f"Exception {e}")
    elif "text" in file.content_type:
        content = file.read()
        yield splitter.split_text(content.decode("utf-8"))
    else:
        return
    
async def ocr_read(file: UploadFile):
    doc = DocumentFile.from_pdf(file=file)
    return predictor(doc)
    
