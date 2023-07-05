from fastapi import APIRouter, UploadFile, File
import openai
import io
import os
from pypdf import PdfReader
from nomic import atlas, login
import numpy as np

router = APIRouter()

openai.api_key = os.getenv("OPENAI_API_KEY")
login(os.getenv("ATLAS_API_KEY"))

@router.post("/v1/embeddings")
async def embed_doc(file: UploadFile = File(...)):    
    #for now just truncate based on length of words
    content = await file.read()
    response = openai.Embedding.create(input = content.decode("utf-8"), model = "text-embedding-ada-002")
    emb = np.array(response['data'][0]['embedding'])
    embeddings = np.random.rand(*emb.shape,2048)
    return atlas.map_embeddings( embeddings=embeddings)