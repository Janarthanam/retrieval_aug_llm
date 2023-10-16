from fastapi import UploadFile
from db.vector_store import Store
from celery import Celery
import os
from langchain.schema import Document
from parsers.document_parsers import Parser, TextParser
import asyncio

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="index_doc")
def index_doc(name, content_type, bytes, file_name):
    db = Store.get_instance().get_collection(name)

    docs = asyncio.run(Parser.get_instance(content_type).parse(bytes, file_name))
        
    for doc in docs:
        print(type(doc))
        db.add_documents([doc])