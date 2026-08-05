"""
Configura ChromaDB con embeddings locales (sentence-transformers).
No requiere API key — los embeddings se generan en la máquina.
"""

import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

COLLECTION_NAME = "onboarding_docs"
CHROMA_PATH = "./chroma_db"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

_client: chromadb.PersistentClient | None = None
_collection: chromadb.Collection | None = None


def get_collection() -> chromadb.Collection:
    global _client, _collection
    if _collection is None:
        embedding_fn = SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
        _client = chromadb.PersistentClient(path=CHROMA_PATH)
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn,
        )
    return _collection


def collection_is_empty() -> bool:
    return get_collection().count() == 0
