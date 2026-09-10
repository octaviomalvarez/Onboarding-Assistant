from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import asyncio
import aiofiles

from rag.ingest import ingest

router = APIRouter()

DOCS_DIR = Path(__file__).parent.parent.parent / "data" / "docs"


@router.get("/admin/docs", response_model=list[str])
def list_docs():
    if not DOCS_DIR.exists():
        return []
    return sorted(f.name for f in DOCS_DIR.glob("*.md"))


@router.post("/admin/docs", status_code=201)
async def upload_doc(file: UploadFile = File(...)):
    if not file.filename or not file.filename.endswith(".md"):
        raise HTTPException(status_code=400, detail="Solo se aceptan archivos .md")
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    dest = DOCS_DIR / file.filename
    async with aiofiles.open(dest, "wb") as f:
        content = await file.read()
        await f.write(content)
    return {"filename": file.filename}


@router.delete("/admin/docs/{filename}")
def delete_doc(filename: str):
    path = DOCS_DIR / filename
    if not path.exists() or not path.name.endswith(".md"):
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    path.unlink()
    return {"deleted": filename}


@router.post("/admin/reindex")
async def reindex():
    def _run():
        ingest(str(DOCS_DIR))
        from rag.store import get_collection
        col = get_collection()
        return col.count()

    total = await asyncio.to_thread(_run)
    docs = sorted(f.name for f in DOCS_DIR.glob("*.md")) if DOCS_DIR.exists() else []
    return {"chunks": total, "sources": docs}
