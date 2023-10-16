from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Body
from fastapi.responses import JSONResponse
import openai
import io
import os
from langchain.schema import Document
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from db.vector_store import Store

router = APIRouter()
_chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff", verbose=True)


@router.get("/v1/datasets/{name}/answer")
async def answer(name: str, query: str):
    """ Answer a question from the doc
    Parameters:
    - `name` of the doc.
    - `query` to be answered.
    Return:
      a string answer to the query
    """
    _db = Store.get_instance().get_collection(name)
    print(query)
    docs = _db.similarity_search_with_score(query=query)
    print(docs)
    answer = _chain.run(input_documents=[tup[0] for tup in docs], question=query)
    return JSONResponse(status_code=200, content={"answer": answer, "metadata": [
        {"file": d[0].metadata['file'], "page" : d[0].metadata['page'], "score": d[1]} for d in docs]}) 


@router.get("/v1/datasets")
async def list() -> list[dict]:
    """ List all the datasets avaialble to query.
    :return:
        list of datasets
    """
    #TODO surface more metadata for individual datasets
    return Store.get_instance().list_collections()