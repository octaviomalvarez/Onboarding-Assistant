"""
Busca los chunks más relevantes para una consulta dada.
Devuelve el contexto listo para incluir en el prompt de Claude.
"""

from .store import get_collection


RELEVANCE_THRESHOLD = 0.75


def retrieve_context(query: str, n_results: int = 3) -> str:
    """
    Busca en ChromaDB los chunks más similares a la query.
    Solo incluye resultados con distancia menor al umbral de relevancia.
    """
    collection = get_collection()

    if collection.count() == 0:
        return ""

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    parts = []
    for doc, meta, dist in zip(documents, metadatas, distances):
        if dist > RELEVANCE_THRESHOLD:
            continue
        source = meta.get("source", "documento interno")
        title = meta.get("title", "")
        parts.append(f"[Fuente: {source}][Título: {title}]\n{doc}")

    return "\n\n---\n\n".join(parts)
