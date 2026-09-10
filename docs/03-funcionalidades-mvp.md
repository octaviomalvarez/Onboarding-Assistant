# Funcionalidades del MVP

## Estado actual

| Funcionalidad | Estado | Notas |
|---|---|---|
| Asistente conversacional (chat) | Implementado | Mock (sin API key), Anthropic y LM Studio |
| RAG sobre documentación interna | Implementado | ChromaDB + sentence-transformers, umbral de relevancia 0.75 |
| Documentos de onboarding indexados | Implementado | 7 archivos .md, 31 chunks en `backend/data/docs/` |
| Widget de chat expandible | Implementado | Tamaño normal (320×460) y expandido (520×540) |
| Streaming de respuestas (SSE) | Implementado | Efecto de escritura en tiempo real |
| Renderizado Markdown en chat | Implementado | react-markdown + remark-gfm, tablas, listas, negrita |
| Indicadores de fuente | Implementado | Muestra el documento origen de cada respuesta |
| Historial de conversación | Implementado | Últimos 10 mensajes enviados al LLM |
| Checklist de onboarding | Implementado | Persistencia en SQLite, toggle vía API |
| Dashboard con progreso | Implementado | Calcula progreso en base al checklist |
| Directorio de contactos | Implementado | Datos de ejemplo |
| Panel de administración de docs | Implementado | Upload, delete y re-index desde la UI |
| Teams Tab | Implementado | Headers CSP + X-Frame-Options configurados |
| Autenticación Azure AD | Pendiente | Para el piloto |

## Páginas del frontend

### `/` — Dashboard
Muestra el resumen del progreso: barra de progreso general, tareas por semana y las próximas tareas pendientes. Acceso rápido al asistente.

### `/checklist` — Checklist
Lista de tareas de las primeras dos semanas, organizadas por semana y categoría. El estado se persiste en SQLite vía API (PUT `/api/v1/checklist/{id}`).

**Categorías:**
- **Accesos:** solicitudes de acceso a herramientas y sistemas
- **Capacitaciones:** cursos obligatorios y recomendados
- **Administrativo:** trámites de RRHH y carga de horas
- **Equipo:** reuniones y presentaciones con el equipo

### `/chat` — Asistente
Interfaz de chat con streaming SSE. El backend busca contexto relevante en ChromaDB antes de responder. Las respuestas se renderizan en Markdown con indicadores de fuente.

### `/contactos` — Contactos clave
Directorio con los contactos principales para el onboarding.

### `/admin` — Panel de administración
Permite subir nuevos archivos `.md`, eliminarlos y re-indexar ChromaDB sin tocar el servidor.

## Endpoints del backend

| Método | Ruta | Descripción |
|---|---|---|
| GET | `/api/v1/health` | Estado del servidor |
| POST | `/api/v1/chat` | Envía un mensaje (respuesta completa) |
| POST | `/api/v1/chat/stream` | Envía un mensaje (respuesta en streaming SSE) |
| GET | `/api/v1/checklist` | Lista de tareas del onboarding |
| PUT | `/api/v1/checklist/{id}` | Actualiza el estado completado de una tarea |
| GET | `/api/v1/contacts` | Lista de contactos clave |
| GET | `/api/v1/admin/docs` | Lista archivos .md disponibles |
| POST | `/api/v1/admin/docs` | Sube un archivo .md |
| DELETE | `/api/v1/admin/docs/{filename}` | Elimina un archivo .md |
| POST | `/api/v1/admin/reindex` | Re-genera los embeddings en ChromaDB |

Ver Swagger en `http://localhost:8000/docs` con el servidor corriendo.
