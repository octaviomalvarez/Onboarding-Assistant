"""
Busca los chunks más relevantes para una consulta dada.
Devuelve el contexto listo para incluir en el prompt de Claude.
"""

from .store import get_collection


def retrieve_context(query: str, n_results: int = 3) -> str:
    """
    Busca en ChromaDB los chunks más similares a la query.
    Devuelve un string con el contexto formateado para el prompt.
    """
    collection = get_collection()

    if collection.count() == 0:
        return ""

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    parts = []
    for doc, meta in zip(documents, metadatas):
        source = meta.get("source", "documento interno")
        parts.append(f"[Fuente: {source}]\n{doc}")

    return "\n\n---\n\n".join(parts)
