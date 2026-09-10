"""
Busca los chunks más relevantes para una consulta dada.
Devuelve el contexto listo para incluir en el prompt de Claude.
"""

from .store import get_collection


RELEVANCE_THRESHOLD = 0.75

SOURCE_LABELS: dict[str, str] = {
    "primera-semana.md": "Primera semana",
    "herramientas-accesos.md": "Herramientas y accesos",
    "capacitaciones.md": "Capacitaciones",
    "contactos-clave.md": "Contactos clave",
    "accesos.md": "Guía de accesos",
    "faq.md": "Preguntas frecuentes",
    "herramientas-data.md": "Herramientas de Data",
}


def retrieve_context(query: str, n_results: int = 3) -> tuple[str, list[str]]:
    """
    Busca en ChromaDB los chunks más similares a la query.
    Devuelve (contexto, lista de fuentes) filtrando por umbral de relevancia.
    """
    collection = get_collection()

    if collection.count() == 0:
        return "", []

    results = collection.query(
        query_texts=[query],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    parts = []
    sources = []
    seen_sources: set[str] = set()

    for doc, meta, dist in zip(documents, metadatas, distances):
        if dist > RELEVANCE_THRESHOLD:
            continue
        source = meta.get("source", "documento interno")
        title = meta.get("title", "")
        parts.append(f"[Fuente: {source}][Título: {title}]\n{doc}")
        if source not in seen_sources:
            seen_sources.add(source)
            sources.append(SOURCE_LABELS.get(source, source))

    return "\n\n---\n\n".join(parts), sources
