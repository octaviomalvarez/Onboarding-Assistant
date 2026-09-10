const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type HistoryEntry = { role: "user" | "assistant"; content: string };
type StreamMeta = { hasContext: boolean; sources: string[] };

export async function streamMessage(
  message: string,
  history: HistoryEntry[],
  onChunk: (chunk: string) => void,
  onDone: (meta: StreamMeta) => void
): Promise<void> {
  const res = await fetch(`${API_URL}/api/v1/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, history }),
  });

  if (!res.ok) throw new Error(`Error del servidor: ${res.status}`);
  if (!res.body) throw new Error("Stream no disponible");

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (!line.startsWith("data: ")) continue;
      const raw = line.slice(6).trim();
      if (!raw) continue;
      try {
        const parsed = JSON.parse(raw);
        if (parsed.chunk !== undefined) {
          onChunk(parsed.chunk);
        } else if (parsed.done) {
          onDone({ hasContext: parsed.has_context ?? false, sources: parsed.sources ?? [] });
        } else if (parsed.error) {
          throw new Error(parsed.error);
        }
      } catch (e) {
        if (e instanceof SyntaxError) continue;
        throw e;
      }
    }
  }
}

export async function fetchChecklist(role?: string): Promise<import("./types").ChecklistItem[]> {
  const url = role
    ? `${API_URL}/api/v1/checklist?role=${encodeURIComponent(role)}`
    : `${API_URL}/api/v1/checklist`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Error al cargar checklist");
  const data = await res.json();
  return data.map((item: Record<string, unknown>) => ({
    ...item,
    dueDay: item.due_day,
  }));
}

export async function updateChecklistItem(id: string, completed: boolean): Promise<void> {
  const res = await fetch(`${API_URL}/api/v1/checklist/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed }),
  });
  if (!res.ok) throw new Error("Error al actualizar checklist");
}

export async function fetchAdminDocs(): Promise<string[]> {
  const res = await fetch(`${API_URL}/api/v1/admin/docs`);
  if (!res.ok) throw new Error("Error al cargar documentos");
  return res.json();
}

export async function uploadDoc(file: File): Promise<void> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/api/v1/admin/docs`, { method: "POST", body: form });
  if (!res.ok) throw new Error("Error al subir documento");
}

export async function deleteDoc(filename: string): Promise<void> {
  const res = await fetch(`${API_URL}/api/v1/admin/docs/${encodeURIComponent(filename)}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Error al eliminar documento");
}

export async function reindexDocs(): Promise<{ chunks: number; sources: string[] }> {
  const res = await fetch(`${API_URL}/api/v1/admin/reindex`, { method: "POST" });
  if (!res.ok) throw new Error("Error al re-indexar");
  return res.json();
}
