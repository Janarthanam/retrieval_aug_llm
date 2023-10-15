from celery import Celery
import os
from api.db.vector_store import Store
from langchain.schema import Document

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@Celery.task("index_doc")
def index_doc(name: str, docs: list[Document]):
    db = Store.get_instance().get_collection(name)
    for doc in docs:
        db.add_documents(doc)