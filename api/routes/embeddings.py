from fastapi import APIRouter, UploadFile, File
import openai
import io
import os
from pypdf import PdfReader

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")

@router.post("/v1/embeddings")
async def embed_doc(file: UploadFile = File(...)):    
    #for now just truncate based on length of words
    content = await file.read()
    return openai.Embedding.create(input = content.decode("utf-8"), model = "text-embedding-ada-002")