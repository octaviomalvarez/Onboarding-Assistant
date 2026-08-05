"""
Carga archivos Markdown de data/docs/ y los divide en chunks.
Cada chunk preserva su fuente para poder mostrar referencias en las respuestas.
"""

from pathlib import Path


def load_chunks(docs_dir: str = "data/docs", min_length: int = 60) -> list[dict]:
    """
    Lee todos los .md de docs_dir y devuelve una lista de chunks.
    Cada chunk es un dict con: id, text, source, title.
    """
    chunks = []
    docs_path = Path(docs_dir)

    for file in sorted(docs_path.glob("*.md")):
        content = file.read_text(encoding="utf-8")
        file_chunks = _chunk_markdown(content, file.name)
        chunks.extend(file_chunks)

    return chunks


def _chunk_markdown(content: str, filename: str) -> list[dict]:
    """
    Divide un documento Markdown en chunks semánticos.
    Cada sección (## Título + párrafos siguientes) es un chunk.
    """
    chunks = []
    current_title = filename
    current_parts: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            # Guardar el chunk anterior si tiene contenido
            if current_parts:
                text = "\n".join(current_parts).strip()
                if len(text) >= 60:
                    chunk_id = f"{filename}_{len(chunks)}"
                    chunks.append({"id": chunk_id, "text": f"{current_title}\n{text}", "source": filename, "title": current_title})
            current_title = line.lstrip("# ").strip()
            current_parts = []
        elif line.startswith("# "):
            current_title = line.lstrip("# ").strip()
        else:
            current_parts.append(line)

    # Último chunk
    if current_parts:
        text = "\n".join(current_parts).strip()
        if len(text) >= 60:
            chunk_id = f"{filename}_{len(chunks)}"
            chunks.append({"id": chunk_id, "text": f"{current_title}\n{text}", "source": filename, "title": current_title})

    return chunks
