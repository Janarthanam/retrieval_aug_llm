from db.vector_store import Store
from celery import Celery
import os
from langchain.schema import Document
from parsers.document_parsers import Parser
import asyncio

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="index_doc")
def index_doc(name, file, file_name):
    db = Store.get_instance().get_collection(name)
    docs = asyncio.run(Parser.get_instance(file).parse(file, file_name))
        
    for doc in docs:
        db.add_documents(doc)