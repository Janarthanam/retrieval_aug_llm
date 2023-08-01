from collections import namedtuple
from langchain.embeddings import OpenAIEmbeddings, ElasticsearchEmbeddings, SentenceTransformerEmbeddings

Embedding = namedtuple("Embedding",["embedding", "dimension", "distance"])

EMBEDDINGS = {
    'SENTENCE': Embedding(SentenceTransformerEmbeddings(),768, "Cosine"),
    'OPEN_AI': Embedding(OpenAIEmbeddings(), 1563, "Cosine"),
}
                       