"""
Script de ingesta: carga los documentos de data/docs/ en ChromaDB.

Uso:
    cd backend
    python -m rag.ingest

Corré esto cada vez que agregues o modifiques documentos en data/docs/.
"""

from .loader import load_chunks
from .store import get_collection


def ingest(docs_dir: str = "data/docs") -> None:
    collection = get_collection()

    chunks = load_chunks(docs_dir)
    if not chunks:
        print(f"No se encontraron documentos en {docs_dir}")
        return

    # Limpiar la colección antes de reinsertar
    existing = collection.count()
    if existing > 0:
        collection.delete(where={"source": {"$ne": ""}})
        print(f"Colección limpiada ({existing} chunks anteriores eliminados)")

    collection.add(
        documents=[c["text"] for c in chunks],
        ids=[c["id"] for c in chunks],
        metadatas=[{"source": c["source"], "title": c["title"]} for c in chunks],
    )

    print(f"Ingesta completada: {len(chunks)} chunks indexados")
    for source in sorted({c["source"] for c in chunks}):
        count = sum(1 for c in chunks if c["source"] == source)
        print(f"  {source}: {count} chunks")


if __name__ == "__main__":
    ingest()
