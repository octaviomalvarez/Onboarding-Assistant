"use client";

import { useState, useEffect, useRef } from "react";
import { fetchAdminDocs, uploadDoc, deleteDoc, reindexDocs } from "@/lib/api";

export default function AdminPage() {
  const [docs, setDocs] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);
  const [reindexing, setReindexing] = useState(false);
  const [reindexResult, setReindexResult] = useState<{ chunks: number; sources: string[] } | null>(null);
  const [error, setError] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => { loadDocs(); }, []);

  async function loadDocs() {
    try { setDocs(await fetchAdminDocs()); } catch { setError("No se pudieron cargar los documentos"); }
  }

  async function handleUpload(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setUploading(true); setError("");
    try {
      await uploadDoc(file);
      await loadDocs();
    } catch { setError("Error al subir el documento"); }
    finally { setUploading(false); if (fileRef.current) fileRef.current.value = ""; }
  }

  async function handleDelete(filename: string) {
    if (!confirm(`¿Eliminar ${filename}?`)) return;
    try { await deleteDoc(filename); await loadDocs(); }
    catch { setError("Error al eliminar el documento"); }
  }

  async function handleReindex() {
    setReindexing(true); setError(""); setReindexResult(null);
    try { setReindexResult(await reindexDocs()); }
    catch { setError("Error al re-indexar"); }
    finally { setReindexing(false); }
  }

  return (
    <div className="p-8 max-w-2xl">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-gray-900">Administración de documentos</h1>
        <p className="text-gray-400 text-sm mt-1">Gestioná los archivos de conocimiento del asistente</p>
      </div>

      {error && (
        <div className="mb-4 px-4 py-3 rounded-xl text-sm bg-red-50 text-red-600">{error}</div>
      )}

      {/* Documentos actuales */}
      <div className="card p-4 mb-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">Documentos indexados</h2>
        {docs.length === 0 ? (
          <p className="text-sm text-gray-400">No hay documentos cargados</p>
        ) : (
          <ul className="space-y-2">
            {docs.map((doc) => (
              <li key={doc} className="flex items-center justify-between py-1.5 px-2 rounded-lg hover:bg-gray-50">
                <span className="text-sm text-gray-700 flex items-center gap-2">
                  <span style={{ color: "#A100FF" }}>📄</span> {doc}
                </span>
                <button
                  onClick={() => handleDelete(doc)}
                  className="text-xs text-red-400 hover:text-red-600 transition-colors"
                >
                  Eliminar
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>

      {/* Upload */}
      <div className="card p-4 mb-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-3">Subir nuevo documento</h2>
        <div className="flex items-center gap-3">
          <input
            ref={fileRef}
            type="file"
            accept=".md"
            onChange={handleUpload}
            disabled={uploading}
            className="text-sm text-gray-500 file:mr-3 file:py-1.5 file:px-3 file:rounded-lg file:border-0 file:text-sm file:font-medium file:text-white disabled:opacity-50"
            style={{ ["--file-bg" as string]: "#A100FF" }}
          />
          {uploading && <span className="text-xs text-gray-400">Subiendo...</span>}
        </div>
        <p className="text-xs text-gray-400 mt-2">Solo archivos .md (Markdown)</p>
      </div>

      {/* Reindexar */}
      <div className="card p-4">
        <h2 className="text-sm font-semibold text-gray-700 mb-1">Re-indexar ChromaDB</h2>
        <p className="text-xs text-gray-400 mb-3">
          Volvé a generar los embeddings de todos los documentos. Necesario después de agregar o modificar archivos.
        </p>
        <button
          onClick={handleReindex}
          disabled={reindexing}
          className="text-white rounded-xl px-4 py-2 text-sm font-medium transition-opacity hover:opacity-90 disabled:opacity-40"
          style={{ background: "#A100FF" }}
        >
          {reindexing ? "Re-indexando..." : "Re-indexar ahora"}
        </button>
        {reindexResult && (
          <div className="mt-3 p-3 rounded-xl text-sm bg-green-50 text-green-700">
            ✓ {reindexResult.chunks} chunks indexados de {reindexResult.sources.length} documentos
          </div>
        )}
      </div>
    </div>
  );
}
